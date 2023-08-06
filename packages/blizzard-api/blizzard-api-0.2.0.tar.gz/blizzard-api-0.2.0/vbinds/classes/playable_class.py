
"""
vbinds - An interface for working with a playable class.
"""

# built-in
import os
from typing import List

# internal
from .engine import Engine
from .specialization import Specialization


class PlayableClass:
    """ An interface for working with class data. """

    def __init__(self, engine: Engine, class_id: int):
        """ Initialize a class from its numeric identity. """

        self.engine = engine

        # initialize base-class data
        self.data = engine.get_class(class_id)
        assert self.data is not None

        # initialize specialization data
        self.specs = {}
        for spec_idx_data in self.data["specializations"]:
            spec = Specialization(self.engine, spec_idx_data["id"])
            self.specs[spec_idx_data["name"]] = spec

    def roles(self) -> List[str]:
        """ Get the list of roles this class can fulfill. """

        role_list = []
        for spec in self.specs.values():
            role = spec.role()
            if role not in role_list:
                role_list.append(role)
        return role_list

    def __str__(self) -> str:
        """ Turn the class into a String for debugging. """

        assert self.data is not None
        border = "****************************************"
        name_border = "=" * len(self.data["name"])
        lines = [border, name_border, self.data["name"], name_border]
        for spec in self.specs.values():
            lines.append(str(spec))
        lines.append(border)
        return os.linesep.join(lines)


def get_classes(engine: Engine) -> List[PlayableClass]:
    """ Using the query engine, get a list of all playable-class objects. """

    classes = engine.get_classes()
    assert classes is not None

    class_objs = []
    for class_idx_data in classes:
        class_objs.append(PlayableClass(engine, class_idx_data["id"]))
    return class_objs
