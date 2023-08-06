import os
import shutil


import boto3
from botocore.exceptions import ClientError
from io import BytesIO
from tempfile import NamedTemporaryFile
from typing import cast, Dict, List, Sequence

import timeout_decorator
from zuper_commons.fs import AbsDirPath, AbsFilePath, mkdirs_thread_safe, write_ustring_to_utf8_file
from zuper_commons.types import ZException

from duckietown_challenges import (
    ArtefactDict,
    AWSConfig,
    CHALLENGE_PREVIOUS_STEPS_DIR,
    CHALLENGE_TMP_SUBDIR,
    RPath,
    StepName,
)
from duckietown_challenges.utils import friendly_size
from . import logger
from .ipfs_utils import IPFSException
from .misc import guess_mime_type
from .runner_cache import compute_sha256hex, copy_to_cache, get_file_from_cache, only_copy_to_cache

IGNORE_PATTERNS = (".DS_Store",)


def upload_files(
    wd: str, aws_config: AWSConfig, ignore_patterns=IGNORE_PATTERNS, copy_to_machine_cache: bool = True,
):
    """
        wd: directory to search for
    """
    toupload = get_files_to_upload(wd, ignore_patterns=ignore_patterns)
    logger.info(f"{len(toupload)} files to upload.")
    if not aws_config:
        msg = "Not uploading artifacts because AWS config not passed."
        logger.info(msg)
        uploaded = only_copy_to_cache(toupload)
    else:
        uploaded = upload(aws_config, toupload, copy_to_machine_cache=copy_to_machine_cache)

    return uploaded


class CouldNotDownloadAll(ZException):
    pass


def download_artefacts(
    aws_config: AWSConfig,
    steps2artefacts: Dict[StepName, Dict[RPath, ArtefactDict]],
    wd: AbsDirPath,
    use_ipfs: bool,
):
    if use_ipfs:
        import ipfsapi

        client = ipfsapi.connect("127.0.0.1", 5001)
        logger.info("connecting to IPFS peers")
        # peers = [
        #     "/dns4/ipfs.duckietown.org/tcp/4001/ipfs/QmPyoL4ZwaTYtGsvFG8A5fG85tQH5sCHWtexkNVjqa52iK",
        #     "/ip4/129.132.0.37/tcp/4001/ipfs/QmW5P8PZhGYGoyGzAGZNKNTKrvbg8m7Wv4QF4o2ghYmuf9",
        # ]
        peers = []
        for peer in peers:
            logger.info(f"connecting to {peer}")
            res = client.swarm_connect(peer)
            logger.debug(str(res))

    else:
        client = None
    for step_name, artefacts in steps2artefacts.items():
        step_dir = os.path.join(wd, step_name)
        mkdirs_thread_safe(step_dir)
        write_ustring_to_utf8_file("touch", os.path.join(step_dir, "touch"))

        for rpath, data in artefacts.items():
            # logger.debug(data)
            fn = os.path.join(step_dir, rpath)
            dn = os.path.dirname(fn)
            mkdirs_thread_safe(dn)

            sha256hex = data["sha256hex"]
            size = data["size"]
            storage = data["storage"]

            if data["mime_type"] == "ipfs":
                if not use_ipfs:
                    # msg = "Need IPFS for this submission"
                    continue
                else:

                    logger.info(f"getting {sha256hex} ")

                    try:
                        try_to_get_hash(client, sha256hex)
                    except:
                        msg = f"Could not get IPFS hash {sha256hex}"
                        logger.error(msg)
                        raise IPFSException(msg)
                    # res = client.file_ls(sha256hex)

                    # logger.info(f'{sha256hex} -> {res}')
                    #
                    # client.get(sha256hex)
                    # os.rename(sha256hex, fn)

                    fn2 = f"/ipfs/{sha256hex}"
                    #
                    # if not os.path.exists(fn2):
                    #     msg = f'Cannot stat the file {fn2}'
                    #     raise Exception(msg)
                    # else:
                    #     logger.info(f'list ipfs files: {os.listdir(fn2)}')
                    #
                    # logger.info(f'list fn files: {os.listdir(fn)}')

                    if os.path.exists(fn):
                        os.unlink(fn)
                    logger.debug(f"Linking {fn} to {fn2}")
                    os.symlink(fn2, fn)

                    assert os.path.lexists(fn2)
                    assert os.path.exists(fn2)

                    continue

            try:
                get_file_from_cache(fn, sha256hex)
                fs = friendly_size(size)
                logger.debug(f"cache   {fs:>7}   {rpath}")
            except KeyError:

                # no local
                if "s3" in storage:
                    if not aws_config:
                        msg = "I cannot download from S3 because credentials not given."
                        raise CouldNotDownloadAll(msg)
                    else:
                        s3ob = storage["s3"]
                        bucket_name = s3ob["bucket_name"]
                        object_key = s3ob["object_key"]

                        logger.info(f"AWS     {friendly_size(size):>7}   {rpath}")
                        get_object(aws_config, bucket_name, object_key, fn)
                        copy_to_cache(fn, sha256hex)

                    size_now = os.stat(fn).st_size
                    if size_now != size:
                        msg = f"Corrupt cache or download for {data} at {fn}."
                        raise ValueError(msg)
                else:
                    msg = "Not in cache and no way to download"
                    raise CouldNotDownloadAll(msg)


@timeout_decorator.timeout(60)
def try_to_get_hash(client, qm):
    res = client.file_ls(qm)

    logger.info(f"{qm} -> {res}")


def try_s3(aws_config: AWSConfig):
    bucket_name = aws_config["bucket_name"]
    aws_access_key_id = aws_config["aws_access_key_id"]
    aws_secret_access_key = aws_config["aws_secret_access_key"]
    aws_root_path = aws_config["path"]

    s3 = boto3.resource(
        "s3", aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key,
    )

    s = b"initial data"
    data = BytesIO(s)
    logger.debug("trying bucket connection")
    s3_object = s3.Object(bucket_name, os.path.join(aws_root_path, "initial.txt"))
    s3_object.upload_fileobj(data)
    logger.debug("uploaded")


def get_object(aws_config: AWSConfig, bucket_name: str, object_key: str, fn: str):
    aws_access_key_id = aws_config["aws_access_key_id"]
    aws_secret_access_key = aws_config["aws_secret_access_key"]

    s3 = boto3.resource(
        "s3", aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key,
    )
    aws_object = s3.Object(bucket_name, object_key)
    aws_object.download_file(fn)


def get_files_to_upload(path: str, ignore_patterns: Sequence[str] = ()) -> Dict[RPath, str]:
    def to_ignore(rpath_: str) -> bool:

        if "fifos" in rpath_:
            # logger.debug(f"ignoring fifo path: {rpath_}")
            return True
        if rpath_.startswith(CHALLENGE_TMP_SUBDIR):
            # logger.debug(f"ignoring tmp path: {rpath_}")
            return True
        # if rpath_.startswith('tmp'):
        #     logger.debug(f'ignore tmp path: {rpath_}')
        #     return True

        if CHALLENGE_PREVIOUS_STEPS_DIR in rpath_:
            # logger.debug(f" ignoring previous: {rpath_}")

            return True

        for p in ignore_patterns:
            if os.path.basename(rpath_) == p:
                # logger.debug(f" ignoring pattern {p}: {rpath_}")
                return True
        # logger.debug(f"including {rpath_}")
        return False

    toupload: Dict[RPath, str] = {}
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            rpath = os.path.join(os.path.relpath(dirpath, path), f)

            if rpath.startswith("./"):
                rpath = rpath[2:]

            if to_ignore(rpath):
                # logger.debug(f"ignoring {rpath}")
                continue
            else:
                pass
                # logger.debug(f"  adding {rpath}")

            rpath = cast(RPath, rpath)
            toupload[rpath] = os.path.join(dirpath, f)

    return toupload


def upload(
    aws_config: AWSConfig,
    toupload: Dict[RPath, AbsFilePath],
    copy_to_machine_cache: bool = True,
    quiet: bool = False,
) -> List[ArtefactDict]:
    bucket_name = aws_config["bucket_name"]
    aws_access_key_id = aws_config["aws_access_key_id"]
    aws_secret_access_key = aws_config["aws_secret_access_key"]
    # aws_root_path = aws_config['path']
    aws_path_by_value = aws_config["path_by_value"]

    s3 = boto3.resource(
        "s3", aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key,
    )

    uploaded: List[ArtefactDict] = []
    for rpath, realfile0 in toupload.items():

        with NamedTemporaryFile(suffix=os.path.basename(realfile0)) as tf:
            realfile = tf.name
            shutil.copy(realfile0, realfile)

            sha256hex = compute_sha256hex(realfile)
            if copy_to_machine_cache:
                copy_to_cache(realfile, sha256hex)

            # path_by_value
            object_key = os.path.join(aws_path_by_value, "sha256", sha256hex)

            # object_key = os.path.join(aws_root_path, rpath)

            size = os.stat(realfile).st_size
            mime_type = guess_mime_type(realfile)

            aws_object = s3.Object(bucket_name, object_key)
            try:
                aws_object.load()
                # logger.info('Object %s already exists' % rpath)
                status = "known"
                if not quiet:
                    logger.debug(f"{status:>15} {friendly_size(size):>8}  {rpath}")

            except ClientError as e:
                not_found = e.response["Error"]["Code"] == "404"
                if not_found:
                    status = "uploading"
                    if not quiet:
                        logger.debug(f"{status:>15} {friendly_size(size):>8}  {rpath}")
                    aws_object.upload_file(realfile, ExtraArgs={"ContentType": mime_type})

                else:
                    raise
            url = f"http://{bucket_name}.s3.amazonaws.com/{object_key}"
            storage = dict(s3=dict(object_key=object_key, bucket_name=bucket_name, url=url))
            uploaded.append(
                dict(size=size, mime_type=mime_type, rpath=rpath, sha256hex=sha256hex, storage=storage,)
            )

    return uploaded


def object_exists(s3, bucket, key):
    from botocore.exceptions import ClientError

    try:
        s3.head_object(Bucket=bucket, Key=key)
    except ClientError as e:
        return int(e.response["Error"]["Code"]) != 404
    return True
