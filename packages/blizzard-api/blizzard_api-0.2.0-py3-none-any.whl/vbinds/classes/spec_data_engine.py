
"""
vbinds - A query extension for querying class-specialization data.
"""

# built-in
from typing import Optional

# internal
from .query_engine import QueryEngine


class SpecDataEngine(QueryEngine):
    """ Exposes 'Playable Specialization API' queries. """

    def get_specs(self, should_print: bool = False) -> Optional[dict]:
        """ Exposes the 'Playable Specializations Index' API call. """

        return self.static_query("playable-specialization/index", should_print)

    def get_spec(self, spec_id: int,
                 should_print: bool = False) -> Optional[dict]:
        """ Exposes the 'Playable Specializations Index' API call. """

        q_str = "playable-specialization/{}".format(str(spec_id))
        return self.static_query(q_str, should_print)

    def get_talents(self, should_print: bool = False) -> Optional[dict]:
        """ Exposes the 'Talents Index' API call. """

        return self.static_query("talent/index", should_print)

    def get_spell(self, spell_id: int,
                  should_print: bool = False) -> Optional[dict]:
        """ Exposes the 'Spell' API call. """

        return self.static_query("spell/{}".format(str(spell_id)),
                                 should_print)

    def get_talent(self, talent_id: int,
                   should_print: bool = False) -> Optional[dict]:
        """ Exposes the 'Talent' API call. """

        return self.static_query("talent/{}".format(str(talent_id)),
                                 should_print)
