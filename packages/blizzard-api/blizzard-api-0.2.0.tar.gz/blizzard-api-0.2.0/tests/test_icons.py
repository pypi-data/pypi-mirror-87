
"""
vbinds - Test that downloading icons works.
"""

# built-in
import tempfile

# module under test
from vbinds.icons import get_icon, IconSize


def test_get_icon_basic():
    """ Test that downloading icons works. """

    ico_name = "spell_frost_frostshock"
    with tempfile.TemporaryDirectory() as tmp_dir:
        assert get_icon(ico_name, tmp_dir) is not None
        assert get_icon(ico_name, tmp_dir, IconSize.SMALL) is not None
        assert get_icon(ico_name, tmp_dir, IconSize.MEDIUM) is not None
        assert get_icon("bad_spell_name", tmp_dir) is None
