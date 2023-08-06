# coding=utf-8
import subprocess

from zuper_commons.fs import read_ustring_from_utf8_file

from duckietown_build_utils import get_important_env_build_args
from . import logger

#
#
# def build_image(client, path: str, tag: str, dockerfile: str, no_build: bool, no_cache: bool = False):
#     if not no_build:
#         cmd = ["docker", "build", "--pull", "-t", tag, "-f", dockerfile]
#         if no_cache:
#             cmd.append("--no-cache")
#
#         df_contents = read_ustring_from_utf8_file(dockerfile)
#
#         cmd.extend(get_important_env_build_args(df_contents))
#
#         cmd.append(path)
#
#         cmds = " ".join(cmd)
#         m = f"""
#
#         Running command:
#
#         $ {cmds}
#
#
#         """
#
#         logger.debug(m)
#         try:
#             subprocess.check_call(cmd)
#         except subprocess.CalledProcessError as e:
#             logger.error(
#                 f"Cannot run command", cmd=cmd, retcode=e.returncode, stdout=e.stdout, stderr=e.stderr
#             )
#             raise
#
#     image = client.images.get(tag)
#     return image

import os

from docker import DockerClient
from zuper_commons.fs import read_ustring_from_utf8_file
from zuper_commons.timing import now_utc

from duckietown_build_utils import (
    BuildFailed,
    BuildResult,
    docker_push_optimized,
    DockerCompleteImageName,
    get_duckietown_labels,
    parse_complete_tag,
    run_build,
    update_versions,
)
from duckietown_build_utils.misc import get_important_env_build_args_dict
from duckietown_challenges.utils import tag_from_date
from . import logger


__all__ = ["submission_build3"]


def submission_build3(username: str, registry: str, no_cache: bool = False) -> DockerCompleteImageName:
    tag = tag_from_date(now_utc())
    df = "Dockerfile"
    organization = username.lower()
    repository = "aido-submissions-dummy"
    update_versions()

    if registry is None:
        logger.error("had to have explicit registry here")
        registry = "docker.io"

    # complete_image = DockerCompleteImageName(f"{organization}/{repository}:{tag}")
    complete_image = "dummy"
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
    return complete_image
