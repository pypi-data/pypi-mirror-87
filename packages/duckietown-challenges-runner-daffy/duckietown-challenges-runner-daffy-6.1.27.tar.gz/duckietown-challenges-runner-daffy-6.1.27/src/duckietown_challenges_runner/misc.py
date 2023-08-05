import mimetypes
import os

import time
from typing import List

__all__ = ["guess_mime_type", "list_all_files", "EveryOnceInAWhile"]


def guess_mime_type(filename: str) -> str:
    if filename.endswith(".log"):
        return "text/plain"
    mime_type, _encoding = mimetypes.guess_type(filename)

    if mime_type is None:
        if filename.endswith(".yaml"):
            mime_type = "text/yaml"
        else:
            mime_type = "binary/octet-stream"
    return mime_type


def list_all_files(wd: str) -> List[str]:
    return [os.path.join(dp, f) for dp, dn, fn in os.walk(wd) for f in fn]


class EveryOnceInAWhile:
    """ Simple class to do a task every once in a while. """

    def __init__(self, interval: float):
        self.interval = interval
        self.last = 0.0

    def now(self) -> bool:
        n = time.time()
        dt = n - self.last
        if dt > self.interval:
            self.last = n
            return True
        else:
            return False
