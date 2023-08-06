import logging
import os
import sys
from contextlib import contextmanager

import termcolor
from ansi2html import Ansi2HTMLConverter
from zuper_commons.fs import mkdirs_thread_safe, write_ustring_to_utf8_file

from .tee import Tee

__all__ = ["setup_logging"]


def get_FORMAT_datefmt():
    pre = "%(asctime)s|%(name)s|%(filename)s:%(lineno)s|%(funcName)s(): "
    pre = termcolor.colored(pre, attrs=["dark"])
    FORMAT = pre + "%(message)s"
    datefmt = "%H:%M:%S"
    return FORMAT, datefmt


conv = Ansi2HTMLConverter()


@contextmanager
def setup_logging(wd: str):
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    mkdirs_thread_safe(wd)
    f_stderr = os.path.join(wd, "stderr.log")
    f_stdout = os.path.join(wd, "stdout.log")

    my_stderr = Tee(f_stderr, sys.stderr)
    sys.stderr = my_stderr
    my_stdout = Tee(f_stdout, sys.stdout)
    sys.stdout = my_stdout
    ch = logging.StreamHandler(sys.stderr.file)

    ch.setLevel(logging.DEBUG)

    root = logging.getLogger()
    FORMAT, datefmt = get_FORMAT_datefmt()
    formatter = logging.Formatter(FORMAT, datefmt=datefmt)
    ch.setFormatter(formatter)
    root.addHandler(ch)

    try:
        yield
    finally:
        my_stdout.flush()
        my_stderr.flush()

        sys.stderr = old_stderr
        sys.stdout = old_stdout
        root.removeHandler(ch)

    def convert(log):
        fn = os.path.splitext(log)[0] + ".html"
        if not os.path.exists(log):
            data = f"There was no output produced. File not found: {log}"
        else:

            data = open(log).read().strip()

            if not data:
                data = "(No output was produced.)"

            data = f"Conversion of log {log}.\n\n{data}"
        # noinspection PyBroadException
        try:

            html = conv.convert(data)
            write_ustring_to_utf8_file(html, fn)

        except:
            pass
        # os.remove(log)

    convert(f_stdout)
    convert(f_stderr)
