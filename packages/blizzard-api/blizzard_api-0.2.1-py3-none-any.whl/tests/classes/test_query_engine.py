
"""
vbinds - Tests game-data queries.
"""

# internal
from tests.environment import get_new_cache

# module under test
from vbinds.classes.query_engine import QueryEngine


def test_query_engine_basic():
    """ Test some static queries to the blizzard API. """

    engine = QueryEngine(get_new_cache())
    assert engine.static_query("playable-class/index", True) is not None
    assert engine.static_has("playable-class/index")
    assert engine.static_query("playable-class/index", True) is not None
    assert engine.static_query("not/a/real/api") is None
    engine.cache.save()
    new_engine = QueryEngine(engine.cache)
    assert new_engine.static_has("playable-class/index")
    engine.cache.clean()
