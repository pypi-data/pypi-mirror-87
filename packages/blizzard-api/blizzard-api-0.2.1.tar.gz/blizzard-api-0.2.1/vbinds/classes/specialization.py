
"""
vbinds - An interface for working with a playable specializations.
"""

# built-in
import os

# internal
from .engine import Engine


def level_to_index(level: int) -> int:
    """ From a talen row's 'level', get the one-indexed translation. """

    level_data = {
        15: 1,
        25: 2,
        30: 3,
        35: 4,
        40: 5,
        45: 6,
        50: 7,
    }
    return level_data[level]


class Specialization:
    """ An interface for working with spec data. """

    def __init__(self, engine: Engine, spec_id: int):
        """ Initialize spec data from its numeric identity. """

        self.engine = engine
        self.data = engine.get_spec(spec_id)
        assert self.data is not None

        # build the talent rows
        self.talent_rows = {}
        for tier_data in self.data["talent_tiers"]:
            # store talents as one-indexed
            talent_row = {}
            for talent_data in tier_data["talents"]:
                talent_index = talent_data["column_index"] + 1
                talent = "TODO"
                talent_row[talent_index] = talent

            # save tiers as one-indexed
            index = level_to_index(tier_data["level"])
            self.talent_rows[index] = talent_row

    def role(self) -> str:
        """
        Determine the role (i.e. 'Damage', 'Tank', 'Healer') for this spec.
        """

        assert self.data is not None
        return self.data["role"]["name"]

    def __str__(self) -> str:
        """ Turn the spec into a String for debugging. """

        assert self.data is not None
        title = "{} ({})".format(self.data["name"], self.data["role"]["name"])
        name_border = "-" * len(title)
        lines = [name_border, title, name_border]

        # build the talent-tree "table"
        for row_idx, row_data in self.talent_rows.items():
            lines.append("{}:".format(row_idx))
            for talent_idx, talent_data in row_data.items():
                lines.append("    {}: {}".format(talent_idx, str(talent_data)))

        return os.linesep.join(lines)
