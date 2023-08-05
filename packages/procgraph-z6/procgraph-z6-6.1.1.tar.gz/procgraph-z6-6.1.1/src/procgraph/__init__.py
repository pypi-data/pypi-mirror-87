""" ProcGraph: what you would get if Simulink was written in Python
    and was actually useful for dealing with log data. """

__version__ = "6.1.1"

from zuper_commons.logs import ZLogger

logger = ZLogger(__name__)
import os

path = os.path.dirname(os.path.dirname(__file__))
logger.info(f"procgraph version {__version__} path {path}")

# If true, does not allow .pgc caches
deny_pgc_cache = False

from .core.exceptions import *

from .core.block import Block, Generator
from .core.model import Model

from .core.model_loader import pg_add_this_package_models

from .core.registrar_other import register_model_spec, register_simple_block, simple_block

from .core.registrar import Library, default_library

from .scripts import pg

from .core.import_magic import import_magic, import_succesful, import_successful

from .core.constants import *

from .block_utils import IteratorGenerator

from .components import *
