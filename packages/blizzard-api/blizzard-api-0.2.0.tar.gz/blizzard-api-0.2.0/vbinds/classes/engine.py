
"""
vbinds - A collection of all implemented query extensions.
"""

# built-in
import os

# internal
from . import DEFAULT_CACHE
from .cache import Cache
from .class_data_engine import ClassDataEngine
from .spec_data_engine import SpecDataEngine


class Engine(ClassDataEngine, SpecDataEngine):
    """ Doesn't implement anything, just aggregates functionality. """


def engine_from_output_root(output_dir: str) -> Engine:
    """
    Build a query engine by constructing a cache and calling the constructor.
    """

    output_dir = os.path.abspath(output_dir)
    return Engine(Cache(os.path.join(output_dir, DEFAULT_CACHE)))
