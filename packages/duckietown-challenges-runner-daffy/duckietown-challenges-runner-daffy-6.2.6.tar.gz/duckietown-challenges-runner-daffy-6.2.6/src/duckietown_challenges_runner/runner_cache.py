import os
import shutil

# cache_max_size_gb = 3
import subprocess
from typing import Dict, List

from zuper_commons.fs import mkdirs_thread_safe

from duckietown_challenges import ArtefactDict, RPath
from . import logger
from .misc import guess_mime_type

cache_dir = "/tmp/duckietown/DT18/evaluator/cache"
cache_dir_by_value = os.path.join(cache_dir, "by-value", "sha256hex")

disable_cache = False


def only_copy_to_cache(toupload: Dict[RPath, str]) -> List[ArtefactDict]:
    uploaded: List[ArtefactDict] = []
    for rpath, realfile in toupload.items():
        sha256hex = compute_sha256hex(realfile)
        copy_to_cache(realfile, sha256hex)
        size = os.stat(realfile).st_size
        mime_type = guess_mime_type(realfile)
        storage = {}
        uploaded.append(
            dict(size=size, mime_type=mime_type, rpath=rpath, sha256hex=sha256hex, storage=storage,)
        )
    return uploaded


def compute_sha256hex(filename) -> str:
    cmd = ["shasum", "-a", "256", filename]
    res: bytes = subprocess.check_output(cmd)
    res2 = res.decode("utf-8")
    tokens = res2.split()
    h = tokens[0]
    assert len(h) == len("08c1fe03d3a6ef7dbfaccc04613ca561b11b5fd7e9d66b643436eb611dfba348")
    return h


def get_file_from_cache(fn, sha256hex):
    """ raises KeyError """

    if disable_cache:
        logger.warning("Forcing cache disabled.")
        msg = "cache disabled"
        raise KeyError(msg)
    mkdirs_thread_safe(cache_dir_by_value)
    have = os.path.join(cache_dir_by_value, sha256hex)
    if os.path.exists(have):
        shutil.copy(have, fn)
    else:
        msg = "Hash not in cache"
        raise KeyError(msg)


def copy_to_cache(fn: str, sha256hex: str):
    if disable_cache:
        logger.warning("Forcing cache disabled.")
        return

    mkdirs_thread_safe(cache_dir_by_value)
    have = os.path.join(cache_dir_by_value, sha256hex)
    if not os.path.exists(have):
        # fs = friendly_size(os.stat(fn).st_size)
        # msg = f"Copying {fs} to cache {have}"
        # logger.debug(msg)
        shutil.copy(fn, have)
