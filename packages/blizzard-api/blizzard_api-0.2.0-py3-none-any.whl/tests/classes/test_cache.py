
"""
vbinds - Tests for the data cache.
"""

# internal
from tests.environment import get_new_cache

# module under test
from vbinds.classes.cache import Cache


def test_cache_basic():
    """ Test that a second cache-load will have the correct data. """

    cache = get_new_cache()
    test_data = cache.get("test")
    test_data["a"] = "a"
    test_data["b"] = "b"
    test_data["c"] = "c"
    cache.save()

    new_cache = Cache(cache.dir)
    compare_data = new_cache.get("test")
    assert compare_data["a"] == "a"
    assert compare_data["b"] == "b"
    assert compare_data["c"] == "c"

    new_cache.clean()
