
"""
vbinds - An interface for establishing a testing environment.
"""

# built-in
import tempfile

# internal
from vbinds.classes.cache import Cache


def get_new_cache() -> Cache:
    """ Make a temporary directory and construct a new cache with it. """

    return Cache(tempfile.mkdtemp())
