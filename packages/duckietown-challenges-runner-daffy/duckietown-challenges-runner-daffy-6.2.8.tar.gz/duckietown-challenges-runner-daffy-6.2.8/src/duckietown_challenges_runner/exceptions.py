# coding=utf-8
from zuper_commons.types import ZException

__all__ = ["UserError"]


class UserError(ZException):
    """ an error that will be briefly printed"""

    pass
