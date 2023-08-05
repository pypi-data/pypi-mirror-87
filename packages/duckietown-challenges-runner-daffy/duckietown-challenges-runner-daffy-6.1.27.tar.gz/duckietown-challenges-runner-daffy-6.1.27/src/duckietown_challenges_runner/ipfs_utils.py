import os
import traceback

from zuper_commons.types import ZException

from . import logger


class IPFSException(ZException):
    pass


def ipfs_available():
    if os.path.exists("/ipfs"):
        fn = "/ipfs/QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdG/readme"
        # noinspection PyBroadException
        try:
            d = open(fn).read()
        except:
            msg = f"Could not open an IPFS file: {traceback.format_exc()}"
            logger.warning(msg)
            return False

        if "Hello" in d:
            return True
        else:
            logger.warning(d)
            return False
    else:
        logger.warning("/ipfs not found")
        return False
