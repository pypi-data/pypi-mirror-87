from contracts import describe_type

import pickle

from .debug_pickler import find_pickling_error
from .safe_write import safe_write, safe_read


__all__ = ["safe_pickle_dump", "safe_pickle_load"]


def safe_pickle_dump(value, filename, protocol=pickle.HIGHEST_PROTOCOL, **safe_write_options):
    from procgraph import logger

    with safe_write(filename, **safe_write_options) as f:
        try:
            pickle.dump(value, f, protocol)
        except Exception:
            msg = "Cannot pickle object of class %s" % describe_type(value)
            logger.error(msg)
            msg = find_pickling_error(value, protocol)
            logger.error(msg)
            raise


def safe_pickle_load(filename):
    # TODO: add debug check
    with safe_read(filename) as f:
        return pickle.load(f)
        # TODO: add pickling debug
