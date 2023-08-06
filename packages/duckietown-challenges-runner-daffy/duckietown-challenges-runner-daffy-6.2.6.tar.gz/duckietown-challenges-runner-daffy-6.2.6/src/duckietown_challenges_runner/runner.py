import argparse
import copy
import getpass
import json
import multiprocessing
import os
import platform
import random
import shutil
import socket
import sys
import time
import traceback
from datetime import datetime
from multiprocessing import Process
from typing import Callable, Dict, List, Optional, Set, Tuple
from urllib.parse import urlsplit

import yaml
from dateutil.parser import parse
from docker import DockerClient
from docker.models.containers import Container
from zuper_commons.fs import AbsDirPath, mkdirs_thread_safe, write_ustring_to_utf8_file
from zuper_commons.text import box, indent
from zuper_commons.timing import now_utc
from zuper_commons.types import ZException

from duckietown_build_utils import (
    docker_pull_retry,
    DockerCompleteImageName,
    get_complete_tag,
    parse_complete_tag,
)
from duckietown_challenges import (
    ArtefactDict,
    AWSConfig,
    CHALLENGE_DESCRIPTION_DIR,
    CHALLENGE_EVALUATION_OUTPUT_DIR,
    CHALLENGE_PREVIOUS_STEPS_DIR,
    CHALLENGE_RESULTS_DIR,
    CHALLENGE_SOLUTION_OUTPUT_DIR,
    ChallengeDescription,
    ChallengeName,
    ChallengeResults,
    ChallengesConstants,
    dtserver_job_heartbeat,
    dtserver_report_job,
    dtserver_work_submission,
    ENV_CHALLENGE_NAME,
    ENV_CHALLENGE_STEP_NAME,
    ENV_SUBMISSION_ID,
    ENV_SUBMITTER_NAME,
    EvaluationParameters,
    EvaluatorFeaturesDict,
    get_duckietown_server_url,
    JobID,
    NoResultsFound,
    read_challenge_results,
    RPath,
    StepName,
    SubmissionID,
    WorkSubmissionResultDict,
)
from duckietown_docker_utils.docker_run import get_developer_volumes
from . import __version__, logger
from .constants import LABEL_CREATED_BY_RUNNER, LABEL_RUNNER_NAME
from .docker_compose import (
    DockerComposeFail,
    get_services_id,
    run_docker,
    write_logs,
)
from .env_checks import (
    check_docker_environment,
    check_executable_exists,
    InvalidEnvironment,
)
from .exceptions import UserError
from .ipfs_utils import ipfs_available, IPFSException
from .logging_capture import setup_logging
from .logging_worker import write_logs_worker
from .login import do_docker_login
from .misc import list_all_files
from .shell_config import DTShellConstants, read_shell_config
from .types import ContainerName, ServiceName
from .uploading import download_artefacts, get_files_to_upload, try_s3, upload, upload_files


def is_solution_container(container_name: str) -> bool:
    return "solution" in container_name


def get_token_from_shell_config():
    k = DTShellConstants.DT1_TOKEN_CONFIG_KEY

    if k in os.environ:
        # msg = 'Using token passed in environment variable %s' % k
        # logger.debug(msg)
        return os.environ[k]
    else:
        pass

        # msg = 'Could not find the env variable %s; reading shell config.' % k
        # logger.debug(msg)

    shell_config = read_shell_config()
    if shell_config.token_dt1 is None:
        msg = "Please set a Duckietown Token using the command `dts tok set`."
        raise UserError(msg)
    else:
        return shell_config.token_dt1


def dt_challenges_evaluator():
    # noinspection PyBroadException
    try:
        dt_challenges_evaluator_()
    except SystemExit:  # --help
        raise
    except BaseException:
        msg = traceback.format_exc()
        logger.error(msg)
        sys.exit(2)


# noinspection PyBroadException
def dt_challenges_evaluator_(args: List[str] = None, token: str = None):
    # from duckietown_challenges.col_logging import setup_logging
    #
    # setup_logging()
    # logger.info(f"-evaluator {__version__}", args=args, sys_argv=sys.argv)

    usage = """

Usage:

"""
    prog = "dt-challenges-evaluator"
    parser = argparse.ArgumentParser(prog=prog, usage=usage)
    parser.add_argument("--version", action="store_true", default=False)
    parser.add_argument("--continuous", action="store_true", default=False)
    parser.add_argument("--no-pull", dest="no_pull", action="store_true", default=False)
    parser.add_argument("--no-upload", dest="no_upload", action="store_true", default=False)
    parser.add_argument("--no-delete", dest="no_delete", action="store_true", default=False)
    parser.add_argument("--no-cache", dest="no_cache", action="store_true", default=False)
    parser.add_argument("--ipfs", dest="ipfs", action="store_true", default=False)
    parser.add_argument("--one", dest="one", action="store_true", default=False)
    parser.add_argument("--keep-registry", dest="do_not_mess_with_repo", action="store_true", default=False)
    parser.add_argument("--machine-id", default=None, help="Machine name")
    parser.add_argument("--name", default=None, help="Evaluator name")
    parser.add_argument("--impersonate", default=None)
    parser.add_argument("--quota-cpu", type=float, default=None, help="average number of CPUs")
    DEFAULT_TMPDIR = "/tmp/duckietown/DT18/evaluator/executions"

    parser.add_argument("--tmpdir", default=DEFAULT_TMPDIR)
    parser.add_argument("--submission", default=None, help="evaluate this particular submission")
    parser.add_argument(
        "--reset", dest="reset", action="store_true", default=False, help="Reset submission",
    )
    parser.add_argument("--features", default="{}")
    parser.add_argument("--debug-volumes", default=None)
    parsed = parser.parse_args(args=args)
    if parsed.submission and parsed.continuous:
        msg = "Cannot specify both --submission and --continuous."
        raise UserError(msg)
    if parsed.version:
        msg = f"Duckietown Challenges Runner {__version__}"
        from duckietown_challenges import __version__ as dcversion

        msg += f"\nDuckietown Challenges {dcversion}"
        print(msg)
        return

    copy_to_machine_cache = not parsed.no_cache
    check_docker_environment()
    try:
        check_executable_exists("docker-compose")
    except InvalidEnvironment:
        msg = "Could not find docker-compose. Please install it."
        msg += "\n\nSee: https://docs.docker.com/compose/install/#install-compose"
        raise InvalidEnvironment(msg)
    tmpdir = parsed.tmpdir

    try:
        more_features = yaml.load(parsed.features, Loader=yaml.SafeLoader)
    except BaseException as e:
        msg = "Could not evaluate your YAML string."
        raise InvalidEnvironment(msg, cmdline_features=parsed.features) from e

    if not isinstance(more_features, dict):
        msg = "I expected that the features are a dict."
        raise InvalidEnvironment(msg, obtained=more_features)

    do_pull = not parsed.no_pull
    do_upload = not parsed.no_upload
    delete = not parsed.no_delete
    reset = parsed.reset
    precise_str = socket.gethostname()
    if os.getpid() != 1:
        precise_str += f"-{os.getpid()}"

    evaluator_name = (parsed.name or "noname") + "_" + precise_str

    if parsed.machine_id:
        machine_id = parsed.machine_id + "_" + socket.gethostname()
    else:
        machine_id = socket.gethostname()

    allow_host_network = False
    quota_cpu = parsed.quota_cpu
    if token is None:
        token = get_token_from_shell_config()

    if parsed.continuous:

        timeout = 5.0  # seconds
        multiplier = 1.0
        multiplier_grow = 1.5
        max_multiplier = 5
        while True:
            multiplier = min(multiplier, max_multiplier)
            t0 = time.time()
            try:
                go_(
                    None,
                    reset=False,
                    do_upload=do_upload,
                    do_pull=do_pull,
                    more_features=more_features,
                    delete=delete,
                    evaluator_name=evaluator_name,
                    machine_id=machine_id,
                    tmpdir=tmpdir,
                    token=token,
                    debug_volumes=parsed.debug_volumes,
                    impersonate=parsed.impersonate,
                    copy_to_machine_cache=copy_to_machine_cache,
                    allow_host_network=allow_host_network,
                    use_ipfs=parsed.ipfs,
                    do_not_mess_with_repo=parsed.do_not_mess_with_repo,
                    quota_cpu=quota_cpu,
                )
                multiplier = 1.0
                if parsed.one:
                    msg = "Because --one was passed, I will finish here."
                    logger.info(msg)
                    break
            except NothingLeft:
                delta = time.time() - t0

                logger.debug(f"No work for me yet. Server answers in {delta:.1f} seconds.")
                # ndots += 1
                # if ndots == 5:
                #     # sys.stderr.write(' no work for me yet.\n')
                #     ndots = 0
                # time.sleep(timeout * multiplier)
                # logger.info('No submissions available to evaluate.')
            except ConnectionError as e:
                logger.error(e)
                multiplier *= multiplier_grow
            except KeyboardInterrupt:
                break
            except BaseException:
                msg = "Uncaught exception"
                logger.error(msg, e=traceback.format_exc())
                multiplier *= multiplier_grow

            r = random.uniform(0, 2)

            try:
                time.sleep(timeout * multiplier + r)
            except KeyboardInterrupt:
                break

    else:
        if parsed.submission:
            submissions = [parsed.submission]
        else:
            submissions = [None]

        for submission_id in submissions:
            try:

                go_(
                    submission_id,
                    reset=reset,
                    do_upload=do_upload,
                    do_pull=do_pull,
                    more_features=more_features,
                    delete=delete,
                    evaluator_name=evaluator_name,
                    machine_id=machine_id,
                    tmpdir=tmpdir,
                    token=token,
                    debug_volumes=parsed.debug_volumes,
                    impersonate=parsed.impersonate,
                    copy_to_machine_cache=copy_to_machine_cache,
                    allow_host_network=allow_host_network,
                    use_ipfs=parsed.ipfs,
                    do_not_mess_with_repo=parsed.do_not_mess_with_repo,
                    quota_cpu=quota_cpu,
                )
            except NothingLeft as e:
                if submission_id is None:
                    msg = "No submissions available to evaluate."
                else:
                    msg = f"Could not evaluate submission {submission_id}."

                msg += "\n" + str(e)
                logger.error(msg)


class NothingLeft(ZException):
    pass


def get_features(more_features, use_ipfs: bool) -> EvaluatorFeaturesDict:
    import psutil

    features = {}

    machine = platform.machine()
    features["linux"] = sys.platform.startswith("linux")
    features["mac"] = sys.platform.startswith("darwin")
    features["x86_64"] = machine == "x86_64"
    features["armv7l"] = machine == "armv7l"
    meminfo = psutil.virtual_memory()
    # svmem(total=16717422592, available=5376126976, percent=67.8, used=10359984128, free=1831890944,
    # active=7191916544, inactive=2325667840, buffers=525037568, cached=4000509952, shared=626225152)

    features["ram_total_mb"] = int(meminfo.total / (1024 * 1024.0))
    features["ram_available_mb"] = int(meminfo.available / (1024 * 1024.0))
    features["nprocessors"] = psutil.cpu_count()
    cpu_freq = psutil.cpu_freq()
    if cpu_freq is not None:
        # None on Docker
        features["processor_frequency_mhz"] = int(psutil.cpu_freq().max)
    f = psutil.cpu_percent(interval=0.2)
    features["processor_free_percent"] = int(100.0 - f)
    features["p1"] = True

    disk = psutil.disk_usage(os.getcwd())

    features["disk_total_mb"] = disk.total / (1024 * 1024)
    features["disk_available_mb"] = disk.free / (1024 * 1024)
    features["picamera"] = False
    features["nduckiebots"] = False
    features["compute_sims"] = True
    # features['map_3x3'] = False

    if use_ipfs:
        if not ipfs_available():
            msg = "IPFS needed but not found"
            raise UserError(msg)
        else:
            logger.info("OK - IPFS still working well")
        features["ipfs"] = 1

    features["gpu"] = os.path.exists("/proc/driver/nvidia/version")

    for k, v in more_features.items():
        if k in features:
            # msg = f"Using {k!r} = {more_features[k]!r} instead of {features[k]!r}"
            # logger.info(msg)
            pass
        features[k] = v

    # logger.debug(json.dumps(features, indent=4))

    return features


def mtime(fn: str) -> float:
    return os.stat(fn).st_mtime


def upload_process(
    aws_config: AWSConfig,
    token: str,
    dirname: str,
    job_id: JobID,
    machine_id: str,
    process_id: str,
    evaluator_version: str,
    impersonate: bool,
):
    from zuper_commons.logs import setup_logging

    setup_logging()
    logger.info("upload_process", dirname=dirname)
    foundpath2mtime: Dict[RPath, float] = {}

    def good_to_upload(x: RPath) -> bool:
        if x == "runner":
            return False
        if "tmp" in x:
            return False
        if "active.avi" in x:
            return False
        if "firstpass.mp4" in x:
            return False
        if ".mp4.metadata.yaml" in x:
            return False
        return True

    while True:

        _uploaded = []

        # noinspection PyBroadException
        try:
            toupload0 = get_files_to_upload(dirname)
            toupload0 = {k: v for k, v in toupload0.items() if good_to_upload(k)}
            toupload: Dict[RPath, str] = {}
            thistime: Dict[RPath, float] = {}
            updated = set()
            for k, v in toupload0.items():
                thistime[k] = mtime(v)
                ignore = foundpath2mtime.get(k, 0) == thistime[k]
                if k in foundpath2mtime:
                    updated.add(k)
                if not ignore:
                    toupload[k] = v
            if toupload:
                logger.info(f"found {len(toupload)} artefacts to upload", existing_but_updated=updated)

                try:
                    _uploaded = upload(aws_config, toupload, quiet=True)
                except:
                    raise
                else:
                    foundpath2mtime.update(thistime)

        except:
            logger.warning(traceback.format_exc())

        # noinspection PyBroadException
        try:
            # TODO:
            more_features = {}
            features = get_features(more_features, use_ipfs=False)

            res_ = dtserver_job_heartbeat(
                token,
                job_id=job_id,
                machine_id=machine_id,
                process_id=process_id,
                evaluator_version=evaluator_version,
                impersonate=impersonate,
                uploaded=_uploaded,
                features=features,
            )
        except:
            logger.warning(traceback.format_exc())
        else:
            if res_["abort"]:
                break

        time.sleep(random.uniform(10, 15))
    logger.info("upload_process terminated gracefully")


#
# class TermHandler:
#     def __init__(self, *, token, job_id, machine_id, process_id, evaluator_version, impersonate, timeout):
#         self.token = token
#         self.job_id = job_id
#         self.machine_id = machine_id
#         self.process_id = process_id
#         self.evaluator_version = evaluator_version
#         self.impersonate = impersonate
#         self.timeout = timeout
#
#     def sigterm_handler(self, _signo, _stack_frame):
#         s = traceback.format_stack(_stack_frame)
#         msg_ = f"Evaluator received SIGTERM \n\n{s} "
#
#         status = ChallengesConstants.STATUS_JOB_ABORTED
#         cr0 = ChallengeResults(status, msg_, scores={})
#         logger.error(cr0=cr0)
#         dtserver_report_job(
#             token=self.token,
#             job_id=self.job_id,
#             stats=cr0.stats,
#             result=cr0.get_status(),
#             ipfs_hashes=cr0.ipfs_hashes,
#             machine_id=self.machine_id,
#             process_id=self.process_id,
#             evaluator_version=self.evaluator_version,
#             uploaded=[],
#             impersonate=self.impersonate,
#             timeout=self.timeout,
#         )
#
#         # Raises SystemExit(0):
#         sys.exit(23)


def go_(
    submission_id_to_ask: Optional[SubmissionID],
    do_pull: bool,
    more_features,
    do_upload: bool,
    delete: bool,
    reset: bool,
    evaluator_name: str,
    machine_id: str,
    tmpdir: str,
    copy_to_machine_cache: bool,
    quota_cpu: Optional[float],
    token: str = None,
    impersonate: Optional[int] = None,
    debug_volumes: Optional[str] = None,
    allow_host_network: bool = False,
    use_ipfs: bool = False,
    do_not_mess_with_repo: bool = False,
):
    if use_ipfs:
        allow_host_network = True
    features = get_features(more_features, use_ipfs=use_ipfs)
    # if features['processor_free_percent'] < 10:
    #     logger.info(f"Waiting because free CPU is {features['processor_free_percent']}%.")
    #     return

    if token is None:
        token = get_token_from_shell_config()

    url = get_duckietown_server_url()

    if do_not_mess_with_repo:
        logger.info(f"Do not mess with repo")
        server_host = None
    else:
        logger.info(url=url)
        url_parsed = urlsplit(url)
        netloc: str = url_parsed.netloc
        if ":" in netloc:
            server_host, _, _ = netloc.rpartition(":")
        else:
            server_host = netloc
        if not server_host:
            raise ZException(url=url, server_host=server_host)

    logger.info(f"Using server_host", server_host=server_host, url=url)

    evaluator_version = __version__
    process_id = evaluator_name

    timeout_server = 60
    res: WorkSubmissionResultDict = dtserver_work_submission(
        token,
        submission_id_to_ask,
        machine_id,
        process_id,
        evaluator_version,
        features=features,
        reset=reset,
        timeout=timeout_server,
        impersonate=impersonate,
    )

    if "job_id" not in res:
        logger.info("No jobs available", url=url)
        msg = "Could not find jobs."
        raise NothingLeft(msg, res=res)
    job_id = res["job_id"]
    aws_config: Optional[AWSConfig] = res.get("aws_config", None)

    docker_username = os.environ.get("DOCKER_USERNAME", None)
    docker_password = os.environ.get("DOCKER_PASSWORD", None)

    if docker_password and docker_username:
        do_docker_login(docker_username, docker_password)
    else:
        logger.warning("Docker credentials not found in environment")
    #
    # handler = TermHandler(
    #     token=token,
    #     job_id=job_id,
    #     machine_id=machine_id,
    #     process_id=process_id,
    #     evaluator_version=__version__,
    #     impersonate=impersonate,
    #     timeout=timeout_server,
    # )
    # signal.signal(signal.SIGTERM, handler.sigterm_handler)

    cd = None
    ctx = multiprocessing.get_context("spawn")

    submission_id = res["submission_id"]
    wd0 = os.path.join(
        tmpdir,
        res["challenge_name"],
        f"submission{submission_id}",
        f"{res['step_name']}-{evaluator_name}-job{job_id}",
    )
    wd = wd0 + "-a-wd"
    fd = wd0 + "-a-fifos"

    params = (aws_config, token, wd, job_id, machine_id, process_id, evaluator_version, impersonate)
    p = ctx.Process(target=upload_process, args=params, daemon=True)
    p.start()

    def heartbeat():
        _uploaded = []

        # noinspection PyBroadException
        try:
            res_ = dtserver_job_heartbeat(
                token,
                job_id=job_id,
                machine_id=machine_id,
                process_id=process_id,
                evaluator_version=evaluator_version,
                impersonate=impersonate,
                uploaded=[],
                features=features,
            )

            abort = res_["abort"]
            why = res_["why"]
        except:
            logger.warning(traceback.format_exc(), res=res)
        else:
            if abort:
                msg_ = f"The server told us to abort the job because: {why}"
                raise KeyboardInterrupt(msg_)

    cr, uploaded = get_cr(
        res=res,
        wd=wd,
        fd=fd,
        do_upload=do_upload,
        evaluator_name=evaluator_name,
        job_id=job_id,
        delete=delete,
        debug_volumes=debug_volumes,
        do_pull=do_pull,
        copy_to_machine_cache=copy_to_machine_cache,
        allow_host_network=allow_host_network,
        use_ipfs=use_ipfs,
        server_host=server_host,
        cd=cd,
        heartbeat=heartbeat,
        quota_cpu=quota_cpu,
    )

    msg = "Reporting status %s for job %s submission %s.\n\n%s\n\n%s\n\n%s" % (
        cr.get_status(),
        job_id,
        submission_id,
        indent(cr.msg, " msg |"),
        indent(json.dumps(cr.get_stats(), indent=4), "stats |"),
        cr.ipfs_hashes,
    )
    if cr.get_status() != ChallengesConstants.STATUS_JOB_SUCCESS:
        logger.error(msg)
    else:
        logger.info(msg)

    stats = cr.get_stats()
    # REST call to the duckietown chalenges server
    ntries = 5
    interval = 30
    while ntries >= 0:
        # noinspection PyBroadException
        try:
            dtserver_report_job(
                token,
                job_id=job_id,
                stats=stats,
                result=cr.get_status(),
                ipfs_hashes=cr.ipfs_hashes,
                machine_id=machine_id,
                process_id=process_id,
                evaluator_version=evaluator_version,
                uploaded=uploaded,
                impersonate=impersonate,
                timeout=timeout_server,
            )
            break
        except BaseException:
            msg = "Could not report."
            logger.warning(msg, e=traceback.format_exc())
            logger.info(f"Retrying {ntries} more times after {interval} seconds")
            ntries -= 1
            time.sleep(interval + random.uniform(0, 2))


def get_cr(
    res: WorkSubmissionResultDict,
    wd: str,
    fd: str,
    do_upload: bool,
    evaluator_name: str,
    job_id: int,
    delete: bool,
    debug_volumes,
    do_pull: bool,
    copy_to_machine_cache: bool,
    allow_host_network: bool,
    use_ipfs: bool,
    server_host: str,
    quota_cpu: Optional[float],
    cd: Optional[ChallengeDescription],
    heartbeat: Optional[Callable] = None,
) -> Tuple[ChallengeResults, List]:
    aws_config = res["aws_config"]
    if aws_config and do_upload:
        try_s3(aws_config)

    # noinspection PyBroadException
    try:

        challenge_name = res["challenge_name"]
        challenge_step_name = res["step_name"]
        submission_id = res["submission_id"]
        timeout_sec = res["timeout"]
        if timeout_sec is None or timeout_sec == 0:
            msg = f"Invalid timeout {timeout_sec}"
            raise ValueError(msg)

    except BaseException:
        msg = "Uncaught exception."
        logger.error(msg, e=traceback.format_exc())
        status = ChallengesConstants.STATUS_JOB_HOST_ERROR
        return ChallengeResults(status, msg, scores={}), []

    uploaded = []

    # noinspection PyBroadException
    try:

        steps2artefacts = res["steps2artefacts"]
        submitter_name = res["submitter_name"]
        steps2scores = res.get("steps2scores", {})

        locations = res["parameters"]["locations"]
        location = locations[0]
        organization = location["organization"]
        repository = location["repository"]
        tag = location["tag"]
        digest = location["digest"]
        registry = location["registry"]

        if registry == "dockerhub":
            registry = "docker.io"

        solution_container = DockerCompleteImageName(f"{registry}/{organization}/{repository}:{tag}@{digest}")
        logger.info(f"solution_container = {solution_container}")

        mkdirs_thread_safe(wd)
        mkdirs_thread_safe(fd)
        own_logs_dir = os.path.join(wd, "logs", "challenges-runner")

        aws_config = res["aws_config"]

        require_scores = set()

        if cd is not None:
            if len(cd.steps) == 1:
                require_scores = set(_.name for _ in cd.scoring.scores)

        try:

            with setup_logging(own_logs_dir):
                logger.debug("running get_cr()", delete=delete, copy_to_machine_cache=copy_to_machine_cache)
                challenge_parameters_ = EvaluationParameters.from_yaml(res["challenge_parameters"])
                # logger.info(challenge_parameters_=challenge_parameters_)
                rnd = random.randint(1, 1000000)

                project = f"{evaluator_name}-job{job_id}-{rnd}"
                if not do_upload:
                    aws_config = None

                cr = run_single(
                    wd=wd,
                    fd=fd,
                    aws_config=aws_config,
                    steps2artefacts=steps2artefacts,
                    challenge_parameters=challenge_parameters_,
                    solution_container=solution_container,
                    challenge_name=challenge_name,
                    challenge_step_name=challenge_step_name,
                    project=project,
                    do_pull=do_pull,
                    debug_volumes=debug_volumes,
                    timeout_sec=timeout_sec,
                    allow_host_network=allow_host_network,
                    use_ipfs=use_ipfs,
                    server_host=server_host,
                    require_scores=require_scores,
                    heartbeat=heartbeat,
                    quota_cpu=quota_cpu,
                    submission_id=submission_id,
                    submitter_name=submitter_name,
                    steps2scores=steps2scores,
                    evaluator_name=evaluator_name,
                )
        finally:
            if do_upload:
                uploaded = upload_files(wd, aws_config, copy_to_machine_cache=copy_to_machine_cache)

        try:
            cmd = ["down"]
            run_docker(wd, project, cmd)
        except DockerComposeFail:
            logger.warning("While taking down after success:\n\n" + traceback.format_exc())

    except KeyboardInterrupt:
        msg = f"KeyboardInterrupt:\n{traceback.format_exc()}"

        cmd = ["down"]
        if wd is not None:
            try:
                run_docker(wd, project, cmd)
            except DockerComposeFail:
                logger.warning("While taking down after failure:\n\n" + traceback.format_exc())

        logger.error(msg)
        status = ChallengesConstants.STATUS_JOB_ABORTED
        cr = ChallengeResults(status, msg, scores={})

    except IPFSException:
        msg = f"Could not access IPFS data:\n{traceback.format_exc()}"
        logger.error(msg)
        status = ChallengesConstants.STATUS_JOB_HOST_ERROR
        cr = ChallengeResults(status, msg, scores={})

    except BaseException:
        msg = f"Uncaught exception:\n{traceback.format_exc()}"
        logger.error(msg)
        status = ChallengesConstants.STATUS_JOB_HOST_ERROR
        cr = ChallengeResults(status, msg, scores={})
    finally:
        if wd:
            if delete:
                msg = f"I am deleting temporary dir {wd}"
                logger.info(msg, contents=list_all_files(wd))
                if os.path.exists(wd):
                    shutil.rmtree(wd)
            else:
                msg = f"I will not delete temporary dir {wd}"
                logger.info(msg)
        else:
            logger.info("Temp dir wd not set")

    return cr, uploaded


def run_single(
    *,
    wd: AbsDirPath,
    fd: AbsDirPath,
    aws_config: Optional[AWSConfig],
    steps2artefacts: Dict[StepName, Dict[RPath, ArtefactDict]],
    steps2scores: Dict[StepName, Dict[str, object]],
    submitter_name: str,
    challenge_parameters: EvaluationParameters,
    solution_container: DockerCompleteImageName,
    challenge_name: ChallengeName,
    challenge_step_name: StepName,
    submission_id: SubmissionID,
    project: str,
    do_pull: bool,
    server_host: Optional[str],
    evaluator_name: str,
    quiet: bool = False,
    debug_volumes: Optional[str] = None,
    timeout_sec: float,
    require_scores: Set[str],
    quota_cpu: Optional[float],
    allow_host_network: bool = False,
    use_ipfs: bool = False,
    heartbeat: Optional[Callable] = None,
):
    """

    :param evaluator_name:
    :param submitter_name:
    :param submission_id:
    :param steps2scores:
    :param wd:
    :param fd: Directory for fifos
    :param aws_config:
    :param steps2artefacts:
    :param challenge_parameters:
    :param solution_container:
    :param challenge_name:
    :param challenge_step_name:
    :param project:
    :param do_pull:
    :param server_host:
    :param debug_volumes:
    :param timeout_sec:
    :param quota_cpu:
    :param require_scores: Set of scores required for this step to be valid
    :param allow_host_network:
    :param use_ipfs:
    :param heartbeat:
    :param quiet: minimal output

    :return:
    """
    # logger.debug(challenge_parameters=challenge_parameters)
    prepare_dir(wd, aws_config, steps2artefacts=steps2artefacts, steps2scores=steps2scores, use_ipfs=use_ipfs)

    tomonitor: List[ContainerName] = []
    for service_name, service_def in challenge_parameters.services.items():
        if service_def.image == ChallengesConstants.SUBMISSION_CONTAINER_TAG:
            continue
        else:
            if "evaluator" in service_name:
                tomonitor.append(ContainerName(service_name))
    if not tomonitor:
        logger.error(f"Cannot find any container to monitor among {list(challenge_parameters.services)}")

    logger.debug(f"The containers to monitor: {tomonitor}")
    add_extra_environment: Dict[str, str] = {}
    add_extra_environment[ENV_CHALLENGE_NAME] = challenge_name
    add_extra_environment[ENV_CHALLENGE_STEP_NAME] = challenge_step_name
    add_extra_environment[ENV_SUBMISSION_ID] = str(submission_id)
    add_extra_environment[ENV_SUBMITTER_NAME] = submitter_name

    add_extra_environment[ChallengesConstants.SUBMISSION_CONTAINER_TAG] = solution_container

    labels = {
        LABEL_CREATED_BY_RUNNER: "true",
        LABEL_RUNNER_NAME: evaluator_name,
    }
    config = get_config(
        wd=wd,
        fd=fd,
        server_host=server_host,
        challenge_parameters_=challenge_parameters,
        solution_container=solution_container,
        debug_volumes=debug_volumes,
        allow_host_network=allow_host_network,
        add_extra_environment=add_extra_environment,
        use_ipfs=use_ipfs,
        quiet=quiet,
        labels=labels,
    )
    config_yaml = yaml.safe_dump(config, encoding="utf-8", indent=4, allow_unicode=True)
    if isinstance(config_yaml, bytes):
        config_yaml = config_yaml.decode("utf-8")
    # logger.debug('YAML:\n' + config_yaml)

    dcfn_original = os.path.join(wd, "docker-compose.original.yaml")
    dcfn = os.path.join(wd, "docker-compose.yaml")

    # logger.info('Compose file: \n%s ' % compose)
    write_ustring_to_utf8_file(config_yaml, dcfn_original)
    write_ustring_to_utf8_file(config_yaml, dcfn)

    # validate the configuration

    try:
        config_validated = run_docker(wd, project, ["config"], get_output=True).decode("utf-8")
        write_ustring_to_utf8_file(config_validated, dcfn)
        # logger.info(config_orig=config_yaml, config_validated=config_validated)
        valid_config = True
        valid_config_error = None
    except DockerComposeFail:
        valid_config_error = "Could not validate Docker Compose configuration."
        logger.error(valid_config_error, tb=traceback.format_exc())
        valid_config = False

    if do_pull:
        client = DockerClient.from_env()
        for service_name, s in config["services"].items():
            image = s["image"]
            if "dummy" in image:
                continue
            docker_pull_retry(client, image, ntimes=4, wait=5)
    if valid_config:
        services_names = list(challenge_parameters.services)
        # print('services: %s' % services_names)
        cr = run_one(
            wd,
            project,
            services=services_names,
            monitor=tomonitor[0],
            timeout_sec=timeout_sec,
            heartbeat=heartbeat,
            quota_cpu=quota_cpu,
            quiet=quiet,
        )

        write_logs(wd, project, services=config["services"])
    else:
        status = ChallengesConstants.STATUS_JOB_ERROR

        cr = ChallengeResults(status, valid_config_error, scores={})

    if cr.status == ChallengesConstants.STATUS_JOB_SUCCESS:
        found_scores = set(cr.scores)
        missing_scores = require_scores - found_scores
        if missing_scores:
            msg = f"Missing scores."
            logger.error(msg, requires=require_scores, found=found_scores)
            cr.status = ChallengesConstants.STATUS_JOB_ERROR
            cr.msg = msg

    return cr


def get_id_for_service(wd, project, service_name) -> str:
    cmd = ["ps", "-q", service_name]

    try:
        o = run_docker(wd, project, cmd, get_output=True)
        container_id = o.decode().strip()  # \n at the end
        if not container_id:
            msg = f"Cannot get ID for servicee {service_name!r}."
            raise DockerComposeFail(msg, o=o)
    except DockerComposeFail:
        raise
    return container_id


class EvaluatorTimeout(ZException):
    pass


class Workers:
    workers = []


def stream_logs(wd: str, service_name: str, container_id: str, color: str, l: int):
    p = Process(target=write_logs_worker, args=(wd, service_name, container_id, color, l))
    p.start()
    Workers.workers.append(p)


def teminate_workers():
    for p in list(Workers.workers):
        # logger.debug('terminating %s' % p)
        Workers.workers.remove(p)
        p.terminate()
    # logger.debug('terminated all workers.')


# noinspection PyBroadException
def run_one(
    wd: AbsDirPath,
    project: str,
    monitor: ContainerName,
    services: List[ServiceName],
    timeout_sec: float,
    quota_cpu: Optional[float],
    heartbeat: Optional[Callable] = None,
    quiet: bool = False,
):
    """

    :param wd:
    :param project:
    :param monitor:
    :param services:
    :param timeout_sec:
    :param quota_cpu: if it is not None, this is the avg number of cpus
    :param heartbeat:
    :param quiet: minimal output
    :return:
    """
    client = check_docker_environment()

    # noinspection PyBroadException
    try:

        try:
            _pruned = client.networks.prune(filters=dict(until="1h"))
            # logger.debug('pruned: %s' % pruned)
        except BaseException:  # XXX not critical
            pass

        cmd = ["down", "-v"]
        run_docker(wd, project, cmd)
        logger.debug(f"Creating containers {services}")
        cmd = ["up", "--no-start", "--renew-anon-volumes"]
        # here
        run_docker(wd, project, cmd)
        try:
            t0 = time.time()

            client = check_docker_environment()
            service2id = get_services_id(wd, project, services)
            # logger.debug(service2id=service2id)
            enable_quotas = False
            if enable_quotas:
                for service_name, container_id in service2id.items():
                    container: Container = client.containers.get(container_id)
                    container.reload()
                    #
                    # cpu.cfs_quota_us: the total available run-time within a period (in microseconds)
                    # cpu.cfs_period_us: the length of a period (in microseconds)
                    # cpu.stat: exports throttling statistics [explained further below]

                    container.update(cpu_shares=250)

                    if is_solution_container(service_name):
                        M = "8g"
                        container.update(memswap_limit=-1, mem_reservation=M, mem_limit=M)
                        if quota_cpu is not None:
                            # every second
                            cpu_period = 1000 * 1000
                            # get 300% cpu
                            cpu_quota = int(quota_cpu * 1000 * 1000)

                            container.update(cpu_period=cpu_period, cpu_quota=cpu_quota)
                            msg = "Applying CPU quota"
                            logger.debug(
                                msg, service_name=service_name, cpu_period=cpu_period, cpu_quota=cpu_quota,
                            )

            logger.debug(f"Starting services", services=services)
            cmd = ["up", "-d"]
            run_docker(wd, project, cmd)

            visualization_info: Dict[ServiceName, str] = {}
            for service_name, container_id in service2id.items():
                container: Container = client.containers.get(container_id)
                container.reload()
                # noinspection PyUnresolvedReferences
                ports = container.ports
                # {'10123/tcp': [{'HostIp': '0.0.0.0', 'HostPort': '32769'}]}
                logger.debug(f"container ports", service_name=service_name, ports=container.ports)
                for port_proto, forwards in ports.items():
                    for forward in forwards:
                        if "HostPort" in forward:
                            HostPort = forward["HostPort"]

                            msg = (
                                f"   Visualization will be available shortly at http://127.0.0.1:"
                                f"{HostPort}   "
                            )
                            # msg = termcolor.colored(msg, color="blue")
                            msg = "\n" * 10 + box(msg) + "\n" * 2
                            logger.info(msg)
                            visualization_info[service_name] = f"http://127.0.0.1:{HostPort}"

            l = max(len(_) for _ in service2id)

            colors_system = ["purple", "blue", "yellow", "magenta"]
            colors_solutions = ["green"]

            for i, (service_name, service_id) in enumerate(service2id.items()):
                if quiet and (not is_solution_container(service_name)):
                    continue
                if is_solution_container(service_name):
                    series = colors_solutions
                else:
                    series = colors_system
                color = series[i % len(series)]
                stream_logs(wd, service_name, service_id, color=color, l=l)
            exited2 = {}
            heartbeat_interval = 10.0
            last_heartbeat = 0.0

            extra = random.uniform(0, 1)
            while True:
                time.sleep(5 + extra + random.uniform(0, 1))

                if heartbeat:
                    t = time.time()
                    if t - last_heartbeat > heartbeat_interval:
                        heartbeat()
                    last_heartbeat = t
                running = []
                running_details = {}
                for service_name, container_id in service2id.items():
                    if service_name in exited2:
                        continue
                    container = client.containers.get(container_id)

                    stats = container.stats(stream=False)
                    try:
                        memory_stats1 = int(stats["memory_stats"]["usage"] / (1024 * 1024.0))
                        memory_stats = f"{memory_stats1} MB RAM"
                    except KeyError:
                        memory_stats = "n/a"
                    cpu_stats = stats["cpu_stats"]["cpu_usage"]["total_usage"] / (1024 * 1024.0)
                    running_details[service_name] = f"{memory_stats}; cpu {int(cpu_stats)}"

                    if container.status == "running":
                        running.append(service_name)
                    else:
                        container_state = container.attrs["State"]
                        exit_code = container_state["ExitCode"]
                        finished_at = parse(container_state["FinishedAt"])
                        exited2[service_name] = exit_code
                        if exit_code:
                            # wait a little bit before bailing out
                            # maybe the evaluator has better debugging
                            passed = now_utc() - finished_at
                            if (exit_code not in [0, 137, 138, 139]) and passed.total_seconds() < 15:
                                msg = (
                                    f"Container for service {service_name} has exited with code {exit_code}. "
                                    "Waiting a bit before bailing out."
                                )
                                logger.info(msg)
                            else:
                                msg = f'The container "{service_name}" exited with code {exit_code}.\n'
                                if exit_code == 137:
                                    msg += (
                                        "\n\nError code 137 means an out-of-memory error. "
                                        "The container exceeded the memory available to it. "
                                    )
                                    status = ChallengesConstants.STATUS_JOB_HOST_ERROR
                                    cr = ChallengeResults(status, msg, scores={})
                                    return cr
                                if exit_code == 138:
                                    msg += "\n\nError code 138 means that GPU could not be found."
                                    status = ChallengesConstants.STATUS_JOB_HOST_ERROR
                                    cr = ChallengeResults(status, msg, scores={})
                                    return cr
                                if exit_code == 139:
                                    msg += "\n\nError code 139 means GPU memory error."
                                    status = ChallengesConstants.STATUS_JOB_HOST_ERROR
                                    cr = ChallengeResults(status, msg, scores={})
                                    return cr

                                msg += "\n\nLook at the logs for the container to know more about the error."
                                logger.error(msg)

                                if is_solution_container(service_name):
                                    status = ChallengesConstants.STATUS_JOB_FAILED
                                    cr = ChallengeResults(status, msg, scores={})
                                    return cr

                                status = ChallengesConstants.STATUS_JOB_HOST_ERROR
                                cr = ChallengeResults(status, msg, scores={})
                                return cr

                delta = time.time() - t0
                msg = f"Running for {int(delta)} s (timeout: {int(timeout_sec)} s)."
                logger.info(
                    msg,
                    running_details=running_details,
                    exited=exited2,
                    visualization_info=visualization_info,
                )

                if monitor in exited2:
                    logger.info(f"The container to monitor {monitor!r} has exited; bye bye.", exited=exited2)
                    break

                if delta > timeout_sec:
                    msg = f"Waited {int(delta)} seconds for container to finish. Giving up. "
                    logger.error(msg)
                    status = ChallengesConstants.STATUS_JOB_ERROR
                    cr = ChallengeResults(status, msg, scores={})
                    return cr

            try:
                cr = read_challenge_results(wd)
            except NoResultsFound as e:
                msg = f"""\
    The result file is not found in working dir {wd}:

    {e}

    This usually means that the evaluator did not finish and some times that there was an import error.
    Check the evaluator log to see what happened."""
                l = "\n".join("-" + f for f in list_all_files(wd))
                msg += f"\n\nList of all files:\n\n {l}"
                logger.error(msg)
                status = ChallengesConstants.STATUS_JOB_ERROR
                cr = ChallengeResults(status, msg, scores={})

        finally:
            pass
            # logger.info("calling down")
            # try:
            #
            #     cmd = ["down", "-v"]
            #     run_docker(wd, project, cmd)
            # except:
            #     logger.warn(traceback.format_exc())

    except DockerComposeFail as e:
        msg = f"Error while running Docker Compose:\n\n{e}"
        logger.error(msg)
        status = ChallengesConstants.STATUS_JOB_HOST_ERROR
        cr = ChallengeResults(status, msg, scores={})

    except KeyboardInterrupt:
        msg = f"KeyboardInterrupt:\n{traceback.format_exc()}"
        logger.error(msg)
        status = ChallengesConstants.STATUS_JOB_ABORTED
        cr = ChallengeResults(status, msg, scores={})

    except BaseException:
        msg = f"Uncaught exception while running Docker Compose:\n{traceback.format_exc()}"
        logger.error(msg)
        status = ChallengesConstants.STATUS_JOB_HOST_ERROR
        cr = ChallengeResults(status, msg, scores={})
    finally:
        teminate_workers()

    return cr


def prepare_dir(
    wd: AbsDirPath,
    aws_config: Optional[AWSConfig],
    steps2artefacts: Dict[StepName, Dict[RPath, ArtefactDict]],
    steps2scores: Dict[StepName, Dict[str, object]],
    use_ipfs: bool,
):
    mkdirs_thread_safe(wd)
    # output for the sub
    challenge_solution_output_dir = os.path.join(wd, CHALLENGE_SOLUTION_OUTPUT_DIR)
    # the yaml with the scores
    challenge_results_dir = os.path.join(wd, CHALLENGE_RESULTS_DIR)
    # the results of the "preparation" step
    challenge_description_dir = os.path.join(wd, CHALLENGE_DESCRIPTION_DIR)
    challenge_evaluation_output_dir = os.path.join(wd, CHALLENGE_EVALUATION_OUTPUT_DIR)
    previous_steps_dir = os.path.join(wd, CHALLENGE_PREVIOUS_STEPS_DIR)

    for d in [
        challenge_solution_output_dir,
        challenge_results_dir,
        challenge_description_dir,
        challenge_evaluation_output_dir,
        previous_steps_dir,
    ]:
        mkdirs_thread_safe(d)
    download_artefacts(aws_config, steps2artefacts, previous_steps_dir, use_ipfs=use_ipfs)
    write_steps_scores(steps2scores, previous_steps_dir)


def write_steps_scores(steps2scores: Dict[StepName, Dict[str, object]], previous_steps_dir: AbsDirPath):
    for step_name, scores in steps2scores.items():
        fn = os.path.join(previous_steps_dir, step_name, "scores.yaml")
        data = yaml.dump(scores)
        write_ustring_to_utf8_file(data, fn)


def get_config(
    wd: AbsDirPath,
    fd: AbsDirPath,
    challenge_parameters_: EvaluationParameters,
    solution_container: DockerCompleteImageName,
    add_extra_environment: Dict[str, str],
    server_host: Optional[str],
    labels: Dict[str, str],
    debug_volumes: Optional[str] = None,
    allow_host_network: bool = False,
    use_ipfs: bool = False,
    quiet: bool = False,
):
    """
        server_host: reachable from other ips
    """
    UID = os.getuid()
    GID = os.getgid()
    USERNAME = getpass.getuser()
    dir_home_guest = f"/fake-home/{USERNAME}"
    rnd = str(random.randint(0, 100000))
    timestamp = datetime.now().strftime("%y_%m_%d_%H_%M_%S")
    dir_fake_home_host = os.path.join(
        f"/tmp/duckietown/dt-challenges-runner/{timestamp}-{rnd}", f"fake-{USERNAME}-home"
    )

    mkdirs_thread_safe(dir_fake_home_host)
    extra_environment = dict(username=USERNAME, uid=UID, USER=USERNAME, HOME=dir_home_guest)

    # Adding the submission container
    for service_name, service_def in challenge_parameters_.services.items():
        service_def.build = None

        if service_def.image == ChallengesConstants.SUBMISSION_CONTAINER_TAG:
            logger.debug("setting solution container", service_name=service_name, service_def=service_def)
            service_def.image = solution_container

    config = challenge_parameters_.as_dict()

    logger.debug(config_begin=config)
    if sys.platform == "darwin":
        additional_mode = ",delegated"
    else:
        additional_mode = ""

    for service_name, service in config["services"].items():
        image = service["image"]
        br = parse_complete_tag(image)
        br.tag = None
        service["image"] = get_complete_tag(br)

        if quiet:
            if not is_solution_container(service_name):
                service["logging"] = {"driver": "none"}

        service.pop("build", None)

        # This is not needed, because the tag is sufficient as it is generated anew.
        # We should perhaps check that we have the right image tag
        #
        # if image_digest is not None:
        #     service['image'] += '@' + image_digest

    # def naturalize(image0: str) -> str:
    #     if "localhost" in image0:
    #         image2 = image0.replace("localhost", server_host)
    #         logger.info(f"replacing {image0} -> {image2}")
    #         # raise Exception(image)
    #         return image2
    #     return image

    # if server_host is not None:
    #     for service in config["services"].values():
    #         service["image"] = naturalize(service["image"])

    use_dev = debug_volumes or ("DT_MOUNT" in os.environ)
    for service in config["services"].values():
        if "labels" not in service:
            service["labels"] = {}
        service["labels"].update(labels)
    # adding extra environment variables:

    for service in config["services"].values():
        service["environment"].update(add_extra_environment)
        service["environment"].update(extra_environment)
        service["user"] = f"{UID}:{GID}"

        if use_dev:
            service["environment"]["PYTHONPATH"] = "/packages"

    volumes0 = {}
    volumes0[wd] = {"bind": "/challenges", "mode": f"rw{additional_mode}"}
    # We write the file so that the other nodes know the paths / mounting are correct
    for d in [fd, wd]:
        write_ustring_to_utf8_file("runner", os.path.join(d, "runner"))

    volumes0[fd] = {"bind": "/fifos", "mode": f"rw{additional_mode}"}
    volumes0[dir_fake_home_host] = {"bind": dir_home_guest, "mode": f"rw{additional_mode}"}

    if use_ipfs:
        if os.path.exists("/ipfs"):
            volumes0["ipfs"] = {"bind": "/ipfs", "mode": f"ro"}
        else:
            msg = "/ipfs mount point not found"
            raise IPFSException(msg)

    if use_dev:
        logger.debug("Mounting local sources.")
        volumes0.update(get_developer_volumes())

    for service in config["services"].values():
        assert "volumes" not in service
        volumes = [f'{k}:{v["bind"]}:{v["mode"]}' for k, v in volumes0.items()]
        service["volumes"] = copy.deepcopy(volumes)

    # logger.info('Now:\n%s' % safe_yaml_dump(config))

    NETWORK_NAME = "evaluation"
    networks_evaluator = dict(evaluation=dict(aliases=[NETWORK_NAME]))
    for service in config["services"].values():

        if allow_host_network:
            service["network_mode"] = "host"
        else:
            service["networks"] = copy.deepcopy(networks_evaluator)
    config["networks"] = dict(evaluation=None)
    # config["volumes"] = dict(fifos=None)
    logger.debug(config_end=config)
    return config
