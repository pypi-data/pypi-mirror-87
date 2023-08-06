
"""
vbinds - Icon-file managing cache.
"""

# built-in
from collections import defaultdict
import logging
import os
import shutil
from typing import Optional

# internal
from vbinds.icons import get_icon
from vbinds.enums import IconSize


class IconCache:
    """ Class for loading icons and tracking which ones have been loaded. """

    log = logging.getLogger(__name__)

    def __init__(self, icon_dir: str):
        """ Load an existing icon cache or construct a new one. """

        self.dir = icon_dir
        os.makedirs(self.dir, exist_ok=True)
        self.data: dict = defaultdict(dict)
        self.load()

    def get(self, name: str, size: IconSize = IconSize.LARGE) -> Optional[str]:
        """ Download an icon and save it to the cache. """

        data = self.data[str(size.value)]
        if not self.has(name, size):
            data[name] = get_icon(name, self.dir, size)
        return data[name]

    def has(self, name: str, size: IconSize = IconSize.LARGE) -> bool:
        """ Check if we have a named-icon in this cache. """

        return name in self.data[str(size.value)]

    def clean(self) -> None:
        """ Remove icons in this cache and clear data. """

        shutil.rmtree(self.dir)
        os.makedirs(self.dir)
        self.data = defaultdict(dict)
        IconCache.log.info("cleaned icon cache at '%s'", self.dir)

    def load(self) -> None:
        """
        Load state from the cache directory, if image-files are already
        present.
        """

        for size in os.listdir(self.dir):
            data = self.data[size]
            size_dir = os.path.join(self.dir, size)
            for icon in os.listdir(size_dir):
                icon_name = icon.replace(".jpg", "")
                full_path = os.path.abspath(os.path.join(size_dir, icon))
                data[icon_name] = full_path
        IconCache.log.debug("loaded icon cache at '%s'", self.dir)
