
"""
vbinds - Tests for icon management.
"""

# built-in
import tempfile

# module under test
from vbinds.classes.icon_cache import IconCache


def test_icon_cache_basic():
    """ Load an icon and make sure that re-loading from a directory works. """

    icon_cache = IconCache(tempfile.mkdtemp())
    assert icon_cache.get("spell_frost_frostshock") is not None
    assert icon_cache.has("spell_frost_frostshock")
    assert icon_cache.get("spell_frost_frostshock") is not None
    second_cache = IconCache(icon_cache.dir)
    assert second_cache.has("spell_frost_frostshock")
    assert second_cache.get("spell_frost_frostshock") is not None
    icon_cache.clean()
