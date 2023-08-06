
"""
vbinds - A simple data cache with file-system backing.
"""

# built-in
from collections import defaultdict
import json
import logging
import os
import shutil
from typing import Dict

# internal
from . import DEFAULT_CACHE


class Cache:
    """ Class for storing dictionary data backed by JSON on disk. """

    log = logging.getLogger(__name__)

    def __init__(self, cache_dir: str = DEFAULT_CACHE):
        """ Load an existing cache or construct a new one. """

        self.dir = cache_dir
        os.makedirs(self.dir, exist_ok=True)
        self.data: Dict[str, dict] = defaultdict(dict)
        self.load()

    def save(self) -> None:
        """ Write each data key to a JSON file in the cache. """

        for key, data in self.data.items():
            full_path = os.path.join(self.dir, "{}.json".format(key))
            with open(full_path, "w") as out_file:
                out_file.write(json.dumps(data))
        Cache.log.info("wrote cache to '%s'", self.dir)

    def load(self) -> None:
        """ Load each JSON file in the cache as data. """

        for filename in os.listdir(self.dir):
            with open(os.path.join(self.dir, filename)) as in_file:
                key = filename.replace(".json", "")
                self.data[key] = json.loads(in_file.read())
        Cache.log.debug("loaded cache at '%s'", self.dir)

    def clean(self) -> None:
        """ Delete the cahce on disk and reset data. """

        shutil.rmtree(self.dir)
        os.makedirs(self.dir)
        self.data = defaultdict(dict)
        Cache.log.info("cleaned cache at '%s'", self.dir)

    def get(self, key: str) -> dict:
        """ Get an existing (or new) top-level key's data. """

        return self.data[key]
