# coding=utf-8
import argparse
import logging
import os
import random
import shutil
import subprocess
import sys
from datetime import datetime
from typing import cast

import termcolor
import yaml
from docker import DockerClient
from zuper_commons.fs import mkdirs_thread_safe, read_ustring_from_utf8_file, write_ustring_to_utf8_file
from zuper_commons.text import indent
from zuper_commons.timing import now_utc
from zuper_commons.types import ZValueError

from duckietown_build_utils import (
    BuildFailed,
    DockerCompleteImageName,
    get_duckietown_labels,
    get_important_env_build_args_dict,
    run_build,
    update_versions,
)
from duckietown_challenges import (
    CHALLENGE_PREVIOUS_STEPS_DIR,
    ChallengeResults,
    dtserver_get_compatible_challenges,
    get_challenge_description,
    List,
    read_submission_info,
    SubmissionID,
    traceback,
)
from duckietown_challenges.utils import tag_from_date
from . import logger
from .exceptions import UserError
from .runner import get_token_from_shell_config, run_single
from .submission_build import submission_build3

usage = """




"""


# noinspection PyBroadException
def runner_local_main():
    try:
        runner_local_main_()
    except UserError as e:
        sys.stdout.flush()
        sys.stderr.flush()
        sys.stderr.write(termcolor.colored(str(e), "red") + "\n")
        sys.exit(1)
    except BaseException:
        sys.stdout.flush()
        sys.stderr.flush()
        s = traceback.format_exc()
        sys.stderr.write(termcolor.colored(s, "red") + "\n")
        sys.exit(2)


def runner_local_main_(args: List[str] = None, token: str = None, docker_username: str = "dummy-user"):
    if args is None:
        from duckietown_challenges.col_logging import setup_logging_color

        setup_logging_color()
    prog = "dts challenges evaluate"

    # logger.info(env=dict(os.environ))
    parser = argparse.ArgumentParser(prog=prog, usage=usage)

    group = parser.add_argument_group("Basic")

    group.add_argument("--no-cache", action="store_true", default=False, help="")

    group.add_argument("--no-build", action="store_true", default=False, help="")
    group.add_argument("--no-pull", action="store_true", default=False, help="")
    group.add_argument("--dev", action="store_true", default=False, help="Activate development mode")
    group.add_argument("--output", default=None)
    group.add_argument("--impersonate", default=None)

    group.add_argument("--challenge", default=None, help="override challenge")
    parser.add_argument("--debug-volumes", default=None)

    parser.add_argument("--quota-cpu", type=float, default=None, help="average number of CPUs")
    parser.add_argument(
        "--quiet", default=False, action="store_true", help="Quiet output (only solution container)"
    )

    group.add_argument("-C", dest="change", default=None)

    evaluator_name = "local"

    parsed = parser.parse_args(args=args)
    quota_cpu = parsed.quota_cpu
    quiet = parsed.quiet

    if quiet:
        logger.setLevel(logging.INFO)

    if parsed.change:
        curdir = os.getcwd()

        logger.debug("Changing dir", current=curdir, to=parsed.change)

        if not os.path.exists(parsed.change):
            msg = "Cannot find dir to change to"
            raise ZValueError(msg, curdir=curdir, tochange=parsed.change)
        os.chdir(parsed.change)

    if token is None:
        token = get_token_from_shell_config()

    path = "."

    sub_info = read_submission_info(path)

    compat = dtserver_get_compatible_challenges(
        token=token, impersonate=parsed.impersonate, submission_protocols=sub_info.protocols, quiet=quiet,
    )
    if not compat.compatible:
        msg = "There are no compatible challenges with submission protocols."
        raise UserError(msg, protocols=sub_info.protocols)

    dockerfile = os.path.join(path, "Dockerfile")
    if not os.path.exists(dockerfile):
        msg = f'I expected to find the file "{dockerfile}".'
        raise Exception(msg)

    # client = check_docker_environment()

    no_cache = parsed.no_cache
    # no_build = parsed.no_build
    do_pull = not parsed.no_pull

    if parsed.challenge is not None:
        sub_info.challenge_names = parsed.challenge.split(",")

    if sub_info.challenge_names is not None:

        for c in sub_info.challenge_names:
            if c not in compat.available_submit:
                msg = f'The challenge "{c}" is not available.'
                # msg += '\n available %s' % list(compat.available_submit)
                raise UserError(msg)

            if c not in compat.compatible:
                msg = f'The challenge "{c}" is not compatible with the protocol {sub_info.protocols}.'
                raise UserError(msg)

    if not sub_info.challenge_names:
        sub_info.challenge_names = compat.compatible

    if len(sub_info.challenge_names) > 1:
        sep = "\n   "
        msg = f"""
This submission can be sent to multiple challenges ({sub_info.challenge_names}).

Therefore, I need you to tell me which challenge to you want to test locally
using the --challenge option.

The options are:
{sep + sep.join(sub_info.challenge_names)}


For example, you could try:

{prog} --challenge {sub_info.challenge_names[0]}

"""
        raise UserError(msg)

    assert sub_info.challenge_names and len(sub_info.challenge_names) == 1, sub_info.challenge_names

    one = sub_info.challenge_names[0]

    logger.debug(f"I will evaluate challenge {one}")
    cd = get_challenge_description(token, one, impersonate=parsed.impersonate)
    # logger.debug(cd=cd)

    # tag = cast(DockerCompleteImageName, "dummy-org/dummy-repo")
    # TODO: change the build procedure
    username = "dummy-org"
    registry = "docker.io"

    solution_container = submission_build3(username, registry, no_cache)

    # image = build_image(
    #     client, tag=tag, path=path, dockerfile=dockerfile, no_cache=no_cache, no_build=no_build,
    # )

    caching = False
    # solution_container = tag
    SUCCESS = "success"
    steps_ordered = list(sorted(cd.steps))
    logger.debug("steps", steps_ordered=steps_ordered)
    output = parsed.output
    if output is None:
        timestamp = datetime.now().strftime("%y_%m_%d_%H_%M_%S")

        output = os.path.join("/tmp/duckietown/dt-challenges-runner/local-evals", one, timestamp)
    logger.info(f"Using output directory {output}")
    for i, challenge_step_name in enumerate(steps_ordered):
        logger.debug(f'Now considering step "{challenge_step_name}"')
        step = cd.steps[challenge_step_name]
        evaluation_parameters_str = (
            yaml.safe_dump(step.evaluation_parameters.as_dict()) + f"\ns: {solution_container}"
        )

        wd_final = os.path.join(output, challenge_step_name)
        if caching:
            params = os.path.join(wd_final, "parameters.json")
            if os.path.exists(wd_final) and os.path.exists(params):
                previous = read_ustring_from_utf8_file(params)

                if previous == evaluation_parameters_str:
                    cr_yaml = open(os.path.join(wd_final, "results.yaml"))
                    cr = ChallengeResults.from_yaml(yaml.load(cr_yaml))
                    if cr.status == SUCCESS:
                        msg = f'Not redoing step "{challenge_step_name}" because it is already completed.'
                        logger.info(msg)
                        msg = f"If you want to re-do it, erase the directory {wd_final}."
                        logger.info(msg)
                        continue
                    else:
                        msg = (
                            f'Breaking because step "{challenge_step_name}" was already evaluated with '
                            f'result "{cr.status}".'
                        )
                        msg += "\n" + f"If you want to re-do it, erase the directory {wd_final}."
                        logger.error(msg)
                        break
                else:
                    logger.info("I will redo the step because the parameters changed.")
                    if os.path.exists(wd_final):
                        shutil.rmtree(wd_final)
        else:
            if os.path.exists(wd_final):
                logger.info("removing", wd_final=wd_final)
                shutil.rmtree(wd_final)

        wd = wd_final + ".tmp"
        fd = wd_final + ".fifos"

        if os.path.exists(fd):
            shutil.rmtree(fd)
        if os.path.exists(wd):
            shutil.rmtree(wd)

        mkdirs_thread_safe(fd)
        logger.info(f"Using working dir {wd}")
        params_tmp = os.path.join(wd, "parameters.json")
        mkdirs_thread_safe(wd)
        write_ustring_to_utf8_file(evaluation_parameters_str, params_tmp)

        previous = steps_ordered[:i]
        for previous_step in previous:
            pd = os.path.join(wd, CHALLENGE_PREVIOUS_STEPS_DIR)
            mkdirs_thread_safe(pd)

            d = os.path.join(pd, previous_step)
            # os.symlink('../../%s' % previous_step, d)
            p = os.path.join(output, previous_step)
            shutil.copytree(p, d)

            mk = os.path.join(d, "docker-compose.yaml")
            if not os.path.exists(mk):
                subprocess.check_call(["find", wd])
                raise Exception()
        aws_config = None
        steps2artefacts = {}
        evaluation_parameters = step.evaluation_parameters
        server_host = None
        if "CONTAINER_PREFIX" in os.environ:
            prefix = os.environ["CONTAINER_PREFIX"]
            # logger.debug(f"will respect CONTAINER_PREFIX = {prefix!r} ")
        else:
            prefix = "noprefix"
            logger.warn(f"did not find CONTAINER_PREFIX; using {prefix!r} ")
        n = random.randint(1, 100000)
        project = f"{prefix}_project{n}"
        if len(cd.steps) == 1:
            require_scores = set(_.name for _ in cd.scoring.scores)
        else:
            require_scores = set()
        submission_id = cast(SubmissionID, 0)
        submitter_name = "local-eval"
        steps2scores = {}
        cr = run_single(
            wd=wd,
            fd=fd,
            aws_config=aws_config,
            steps2artefacts=steps2artefacts,
            challenge_parameters=evaluation_parameters,
            solution_container=solution_container,
            challenge_name=one,
            challenge_step_name=challenge_step_name,
            project=project,
            do_pull=do_pull,
            debug_volumes=parsed.debug_volumes,
            timeout_sec=step.timeout,
            server_host=server_host,
            require_scores=require_scores,
            quota_cpu=quota_cpu,
            quiet=quiet,
            submission_id=submission_id,
            steps2scores=steps2scores,
            submitter_name=submitter_name,
            evaluator_name=evaluator_name,
        )

        fn = os.path.join(wd, "results.yaml")
        with open(fn, "w") as f:
            res = yaml.dump(cr.to_yaml())
            f.write(res)

        s = ""
        s += f"\nStatus: {cr.status}"
        s += "\nScores:\n\n%s" % yaml.safe_dump(cr.scores, default_flow_style=False)
        s += "\n\n%s" % cr.msg
        logger.info(indent(s, dark(f"step {challenge_step_name} : ")))

        os.rename(wd, wd_final)

        if cr.status != SUCCESS:
            logger.error(f'Breaking because step "{challenge_step_name}" has result {cr.status}.')
            break

    outdir = os.path.realpath(output)
    logger.info(f"You can find your output inside the directory\n     {outdir}")


def dark(x):
    return termcolor.colored(x, attrs=["dark"])


def submission_build_2(username: str, registry: str, no_cache: bool = False) -> DockerCompleteImageName:
    tag = tag_from_date(now_utc())
    df = "Dockerfile"
    organization = username.lower()
    # repository = "aido-submissions"
    repository = "dummy-repo"
    update_versions()

    if registry is None:
        logger.error("had to have explicit registry here")
        registry = "docker.io"

    complete_image = cast(DockerCompleteImageName, f"{registry}/{organization}/{repository}:{tag}")

    if not os.path.exists(df):
        msg = f'I expected to find the file "{df}".'
        raise Exception(msg)

    # cmd = ["docker", "build", "--pull", "-t", complete_image, "-f", df]
    path = os.getcwd()
    client = DockerClient.from_env()
    labels = get_duckietown_labels(path)

    df_contents = read_ustring_from_utf8_file(df)

    build_vars = get_important_env_build_args_dict(df_contents)
    args = dict(
        path=path, tag=complete_image, pull=True, buildargs=build_vars, labels=labels, nocache=no_cache
    )
    try:
        run_build(client, **args)
    except BuildFailed:
        raise

    # digest = docker_push_optimized(complete_image)
    # br = parse_complete_tag(digest)
    # br.tag = tag
    # return br
    return complete_image


if __name__ == "__main__":
    runner_local_main()
