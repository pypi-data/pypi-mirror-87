
"""
vbinds - Test the program entry-point.
"""

# built-in
import tempfile

# module under test
from vbinds.entry import main


def test_main_basic():
    """
    Test program functionality and health through the command-line entry.
    """

    assert main(["asdf", "asdf", "asdf"]) != 0

    with tempfile.TemporaryDirectory() as tmp_dir:
        base_args = ["program", "-o", tmp_dir]
        assert main(base_args) == 0
        assert main(base_args + ["-v"]) == 0
        assert main(base_args + ["--version"]) == 0
