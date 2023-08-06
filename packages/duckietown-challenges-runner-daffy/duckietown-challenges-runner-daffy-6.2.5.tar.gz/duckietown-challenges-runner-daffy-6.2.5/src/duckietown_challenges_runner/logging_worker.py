import os
import sys

from ansi2html import Ansi2HTMLConverter
from dateutil import parser as dateutil_parser
from zuper_commons.fs import mkdirs_thread_safe, write_ustring_to_utf8_file
from zuper_commons.timing import now_utc
from zuper_commons.ui import colorize_rgb

from . import __version__, logger
from .docker_compose import exit_code_for_container
from .env_checks import check_docker_environment
from .misc import EveryOnceInAWhile

__all__ = ["write_logs_worker"]


def write_logs_worker(wd: str, service_name: str, container_id: str, color: str, l: int):
    conv = Ansi2HTMLConverter()

    logdir = os.path.join(wd, "logs")

    service_dir = os.path.join(logdir, service_name)
    mkdirs_thread_safe(service_dir)
    combined_log = os.path.join(service_dir, "online.log")
    combined_html = os.path.join(service_dir, "online.html")

    in_a_while = EveryOnceInAWhile(5)

    with open(combined_log, "ab") as f:
        buffer: bytes = b""

        def write(a: bytes):
            nonlocal buffer
            buffer += a
            f.write(a)
            f.flush()

        def do_conversion():

            to_convert = f"Converting logs for for service {service_name} -> container id {container_id}."
            now = now_utc().isoformat()
            to_convert += f"\nLast update: {now}"
            to_convert += f"\n---\n{buffer.decode()}\n---\n"
            to_convert += f"\nLast update: {now}"
            html = conv.convert(to_convert)
            write_ustring_to_utf8_file(html, combined_html)

        write(f"Starting logs for service {service_name} -> container id {container_id}\n\n".encode())
        write(f"runner version: {__version__}\n\n".encode())
        write(f"combined_log: {combined_log}\n\n".encode())
        # logger.info('writing logs for %s ' % container_id)

        scol = colorize_rgb(service_name.ljust(l), rgb=color)
        client = check_docker_environment()

        container = client.containers.get(container_id)

        for x in container.logs(stream=True, stdout=True, stderr=True, timestamps=True):
            buffer += x
            f.write(x)
            f.flush()

            x = x.decode("utf-8")
            i = x.index(" ")
            timestamp = x[:i]
            message = x[i + 1 :].rstrip()  # \n
            ts = dateutil_parser.parse(timestamp)

            s = f"{ts.strftime('%H:%M:%S')} {scol} {message}"
            sys.stdout.write(s + "\n")
            sys.stdout.flush()

            if container.status != "running":
                break

            if in_a_while.now():
                do_conversion()

        exit_code = exit_code_for_container(container_id)
        write(f"\nContainer terminated with {exit_code}".encode())
        do_conversion()

    logger.debug(f"write_logs_worker: container {service_name} terminated with {exit_code}")
