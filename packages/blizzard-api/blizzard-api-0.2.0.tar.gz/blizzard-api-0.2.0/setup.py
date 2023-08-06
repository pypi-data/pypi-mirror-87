
"""
vbinds - Package definition for distribution.
"""

# internal
from vbinds import VERSION, DESCRIPTION
from mk.setup import setup


author_info = {"name": "Vaughn Kottler",
               "email": "vaughnkottler@gmail.com",
               "username": "vkottler"}
pkg_info = {"name": "blizzard-api", "version": VERSION,
            "description": DESCRIPTION}
setup(pkg_info, author_info,
      url_override="https://github.com/vkottler/keybinds/tree/master/wow",
      console_overrides=["bapi=vbinds.entry:main"])
