
"""
vbinds - A query extension for querying class data.
"""

# built-in
from typing import Optional

# internal
from .query_engine import QueryEngine


class ClassDataEngine(QueryEngine):
    """ Exposes 'Playable Class API' queries. """

    def get_classes(self, should_print: bool = False) -> Optional[dict]:
        """ Exposes the 'Playable Class Index' API call. """

        result = self.static_query("playable-class/index", False)
        if result is not None:
            result = result["classes"]
            if should_print:
                self.printer.pprint(result)
        return result

    def get_class(self, class_id: int,
                  should_print: bool = False) -> Optional[dict]:
        """ Exposes the 'Playable Class' API call. """

        return self.static_query("playable-class/{}".format(str(class_id)),
                                 should_print)

    def get_class_media(self, class_id: int,
                        should_print: bool = False) -> Optional[dict]:
        """ Exposes the 'Playable Class Media' API call. """

        q_str = "media/playable-class/{}".format(str(class_id))
        return self.static_query(q_str, should_print)

    def get_class_pvp_talent_slots(
        self, class_id: int, should_print: bool = False
    ) -> Optional[dict]:
        """ Exposes the 'PvP Talent Slots' API call. """

        q_str = "playable-class/{}/pvp-talent-slots".format(str(class_id))
        return self.static_query(q_str, should_print)
