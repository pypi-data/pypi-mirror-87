# coding=utf-8
__version__ = "6.2.6"

from zuper_commons.logs import ZLogger

logger = ZLogger(__name__)

import os

path = os.path.dirname(os.path.dirname(__file__))


logger.debug(f"duckietown_challenges_runner version {__version__} path {path}")
from .runner import dt_challenges_evaluator

from .runner_local import runner_local_main
