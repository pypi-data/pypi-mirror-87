# -*- coding: utf-8 -*-
import logging

logging.basicConfig()
logger = logging.getLogger("duckietown-tokens ")
logger.setLevel(logging.INFO)

__version__ = "6.0.9"

import os

path = os.path.dirname(os.path.dirname(__file__))

logger.debug(f"duckietown-tokens version {__version__} path {path}")

from .duckietown_tokens import *
from .tokens_cli import *
