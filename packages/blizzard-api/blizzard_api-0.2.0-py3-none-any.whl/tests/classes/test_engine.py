
"""
vbinds - Tests high-level queries.
"""

# internal
from tests.environment import get_new_cache

# module under test
from vbinds.classes.engine import Engine


def test_engine_queries():
    """ Test query-engine calls. """

    engine = Engine(get_new_cache())
    assert engine.get_classes(True) is not None
    assert engine.get_class(7) is not None
    assert engine.get_class_media(7) is not None
    assert engine.get_class_pvp_talent_slots(7) is not None
    assert engine.get_talents() is not None
    assert engine.get_specs() is not None
    engine.cache.clean()
