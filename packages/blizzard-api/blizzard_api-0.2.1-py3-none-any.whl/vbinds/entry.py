
"""
vbinds - Package's command-line entry-point.
"""

# built-in
import argparse
import logging
import os
import sys
from typing import List

# internal
from vbinds.classes.icon_cache import IconCache
from vbinds.classes.engine import engine_from_output_root
from vbinds.classes.playable_class import get_classes
from . import DESCRIPTION, VERSION


def main(argv: List[str] = None) -> int:
    """ Program entry-point. """

    result = 0

    # fall back on command-line arguments
    command_args = sys.argv
    if argv is not None:
        command_args = argv

    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument("--version", action="version",
                        version="%(prog)s {0}".format(VERSION))
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="set to increase logging verbosity")
    parser.add_argument("-o", "--out-dir", default=os.getcwd(),
                        help="root directory for program outputs")

    try:
        args = parser.parse_args(command_args[1:])
        args.out_dir = os.path.abspath(args.out_dir)

        # initialize logging
        log_level = logging.DEBUG if args.verbose else logging.INFO
        logging.basicConfig(level=log_level,
                            format=("%(name)-30s - %(levelname)-8s - "
                                    "%(message)s"))

        # initialize an icon cache and query engine
        icon_cache = IconCache(os.path.join(args.out_dir, "icons"))
        engine = engine_from_output_root(args.out_dir)

        icon_cache.get("spell_frost_frostshock")
        icon_cache.get("spell_nature_lightning")

        classes = get_classes(engine)
        for class_data in classes:
            print(class_data)
            print(class_data.roles())

        engine.save()
    except SystemExit as exc:
        result = 1
        if exc.code is not None:
            result = exc.code

    return result
