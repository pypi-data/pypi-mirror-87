__version__ = "6.1.0"

import os

from zuper_commons.logs import ZLogger
import pyparsing

logger = ZLogger(__name__)

path = os.path.dirname(os.path.dirname(__file__))
logger.info(f"version {__version__} path {path} pyparsing {pyparsing.__version__}")

from .language import *

from .language_parse import *
from .language_recognize import *

from .structures import *
from .compatibility import *
