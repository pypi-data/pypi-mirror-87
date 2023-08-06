
"""
vbinds - Tests talent and spell classes.
"""

# internal
from tests.environment import get_new_cache

# module under test
from vbinds.classes.engine import Engine
from vbinds.classes.talent import Talent, Spell


def test_talent_basic():
    """ Test that a talent can be loaded. """

    engine = Engine(get_new_cache())
    talent = Talent(engine, 23106)
    assert talent.name() == "Eye of the Tiger"
    assert str(talent) is not None
    engine.cache.clean()


def test_spell_basic():
    """ Test that a spell can be loaded. """

    engine = Engine(get_new_cache())
    spell = Spell(engine, 263642)
    assert spell.name() == "Fracture"
    assert str(spell) is not None
    engine.cache.clean()
