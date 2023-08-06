
"""
vbinds - An interface for working with usable talents.
"""

# internal
from .engine import Engine


class Spell:
    """ An interface for working with spell data. """

    def __init__(self, engine: Engine, spell_id: int):
        """ Initialize a spell from its numeric identity. """

        self.engine = engine
        self.data = engine.get_spell(spell_id)

    def name(self) -> str:
        """ Get this spell's name. """

        assert self.data is not None
        return self.data["name"]

    def __str__(self) -> str:
        """ Turn the spell into a String for debugging. """

        assert self.data is not None
        return "{} ({}): {}".format(self.data["name"], self.data["id"],
                                    self.data["description"])


class Talent:
    """ An interface for working with talent data. """

    def __init__(self, engine: Engine, talent_id: int):
        """ Initialize a talent from its numeric identity. """

        self.engine = engine
        self.data = engine.get_talent(talent_id)
        assert self.data is not None
        self.spell = Spell(self.engine, self.data["spell"]["id"])

    def name(self) -> str:
        """ Get this talent's name. """

        return self.spell.name()

    def __str__(self) -> str:
        """ Turn the talent into a String for debugging. """

        return str(self.spell)
