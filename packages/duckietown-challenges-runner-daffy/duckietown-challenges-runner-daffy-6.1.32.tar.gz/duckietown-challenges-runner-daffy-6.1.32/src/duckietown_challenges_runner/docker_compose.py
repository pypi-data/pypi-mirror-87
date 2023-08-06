import os
import subprocess
import sys
import tempfile
import traceback
from typing import cast, Dict, List

from docker import DockerClient
from zuper_commons.fs import AbsDirPath, mkdirs_thread_safe, write_ustring_to_utf8_file
from zuper_commons.types import ZException, ZValueError

from . import logger
from .env_checks import check_docker_environment
from .tee import Tee

__all__ = [
    "get_services_id",
    "DockerComposeFail",
    "get_services_id",
    "run_docker",
    "write_logs",
    "exit_code_for_container",
]

from .types import ContainerID, ServiceName


class DockerComposeFail(ZException):
    pass


def get_services_id(
    wd: AbsDirPath, project: str, services: List[ServiceName]
) -> Dict[ServiceName, ContainerID]:
    cmd = ["ps", "-q"]
    cmd.extend(services)

    output = b"not available"
    names = {}
    try:
        try:
            output = run_docker(wd, project, cmd, get_output=True)
        except DockerComposeFail:
            raise
        container_ids = output.decode("utf-8").strip().split("\n")  # \n at the end
        container_ids = cast(List[ContainerID], container_ids)
        # Note: unfortunately the container_ids are not ordered
        res: Dict[ServiceName, ContainerID] = {}
        client = DockerClient.from_env()

        for container_id in container_ids:

            container = client.containers.get(container_id)
            names[container_id] = container.name
            for s in services:
                if s in container.name:
                    res[s] = container_id
        if len(res) != len(services):
            raise ZValueError(container_ids=container_ids, services=services, res=res, names=names)
        return res
    except Exception as e:
        msg = "Cannot get process ids"
        raise DockerComposeFail(msg, output=output.decode(), names=names) from e


def run_docker(cwd: str, project: str, cmd0: List[str], get_output: bool = False) -> bytes:
    """ raises DockerComposeFail """
    cmd0 = ["docker-compose", "-p", project] + cmd0
    # logger.info('Running:\n\t%s' % " ".join(cmd0) + '\n\n in %s' % cwd)
    logger.debug(cwd=cwd, command=" ".join(cmd0))

    d = tempfile.mkdtemp()

    fn1 = os.path.join(d, "docker-stdout.txt")
    fn2 = os.path.join(d, "docker-stderr.txt")
    # logger.debug('Saving stdout to %s' % fn1)

    tee_stdout = Tee(fn1, sys.stdout)
    tee_stderr = Tee(fn2, sys.stderr)

    try:
        if get_output:
            return subprocess.check_output(cmd0, cwd=cwd, stderr=sys.stderr)
        else:
            # noinspection PyTypeChecker
            # subprocess.check_call(cmd0, cwd=cwd, stdout=tee_stdout, stderr=tee_stderr)
            subprocess.check_call(cmd0, cwd=cwd, stdout=sys.stdout, stderr=sys.stderr)
    except subprocess.CalledProcessError as e:
        msg = "Could not run command"
        raise DockerComposeFail(
            msg, cmd=cmd0, stdout=tee_stdout.getvalue(), sderr=tee_stderr.getvalue(), e=str(e)
        ) from e
    finally:
        # noinspection PyBroadException
        try:
            os.unlink(fn1)
            os.unlink(fn2)
        except:
            pass
        pass


def logs_for_container(client: DockerClient, container_id: str, stdout: bool, stderr: bool) -> str:
    container = client.containers.get(container_id)
    logs = container.logs(stdout=stdout, stderr=stderr, timestamps=True)
    return logs.decode("utf-8")


from ansi2html import Ansi2HTMLConverter

conv = Ansi2HTMLConverter()


def write_logs(wd: AbsDirPath, project: str, services: List[ServiceName]):
    client = check_docker_environment()

    logdir = os.path.join(wd, "logs")
    mkdirs_thread_safe(logdir)

    services2id: Dict[ServiceName, ContainerID] = get_services_id(wd, project, services)
    for service in services:
        # noinspection PyBroadException
        try:
            container_id = services2id[service]

            if not container_id:
                logs = f'Service "{service}" was not started.'
                logger.warning(logs)
            else:
                # logger.info('Found container ID = %r' % container_id)
                ops = {
                    "combined": dict(stderr=True, stdout=True),
                    "stderr": dict(stderr=True, stdout=False),
                    "stdout": dict(stdout=True, stderr=False),
                }
                for fname, options in ops.items():
                    logs = logs_for_container(client, container_id, **options)

                    html = conv.convert(logs)

                    logdir_service = os.path.join(logdir, service)
                    mkdirs_thread_safe(logdir_service)
                    fn = os.path.join(logdir_service, f"{fname}.log")
                    write_ustring_to_utf8_file(logs, fn)

                    fn = os.path.join(logdir_service, f"{fname}.html")
                    write_ustring_to_utf8_file(html, fn)
        except:
            logger.error(traceback.format_exc())


def exit_code_for_container(container_id: str):
    cmd = ["docker", "inspect", container_id, "--format={{.State.ExitCode}}"]
    out = subprocess.check_output(cmd)
    return int(out.strip())
