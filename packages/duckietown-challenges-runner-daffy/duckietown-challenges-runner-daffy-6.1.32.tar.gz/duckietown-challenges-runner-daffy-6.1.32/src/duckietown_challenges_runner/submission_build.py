# coding=utf-8
import subprocess

from zuper_commons.fs import read_ustring_from_utf8_file

from duckietown_build_utils import get_important_env_build_args
from . import logger


def build_image(client, path: str, tag: str, dockerfile: str, no_build: bool, no_cache: bool = False):
    if not no_build:
        cmd = ["docker", "build", "--pull", "-t", tag, "-f", dockerfile]
        if no_cache:
            cmd.append("--no-cache")

        df_contents = read_ustring_from_utf8_file(dockerfile)

        cmd.extend(get_important_env_build_args(df_contents))

        cmd.append(path)

        cmds = " ".join(cmd)
        m = f"""

        Running command:

        $ {cmds}


        """

        logger.debug(m)
        try:
            subprocess.check_call(cmd)
        except subprocess.CalledProcessError as e:
            logger.error(
                f"Cannot run command", cmd=cmd, retcode=e.returncode, stdout=e.stdout, stderr=e.stderr
            )
            raise

    image = client.images.get(tag)
    return image
