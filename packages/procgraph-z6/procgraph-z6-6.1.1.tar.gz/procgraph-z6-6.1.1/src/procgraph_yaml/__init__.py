""" YAML conversions. """

procgraph_info = {"requires": ["yaml"]}


from procgraph import import_magic

yaml = import_magic(__name__, "yaml")


from .yaml2object import *
from .object2yaml import *

__all__ = ["yaml2object"]
