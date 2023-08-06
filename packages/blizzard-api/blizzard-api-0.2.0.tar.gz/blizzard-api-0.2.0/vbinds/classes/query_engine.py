
"""
vbinds - A game-data API query orchestrator.
"""

# built-in
import logging
import pprint
from typing import Optional

# third-party
import requests

# internal
from vbinds.enums import (
    Region, Locale, Namespace, get_namespace_str, get_query_str
)
from .token_engine import TokenEngine
from .cache import Cache


class QueryEngine(TokenEngine):
    """ A class for building and executing game-data queries. """

    log = logging.getLogger(__name__)

    def __init__(self, cache: Cache, region: Region = Region.US,
                 locale: Locale = Locale.en_US):
        """
        Build a query engine from a given cache, for a specific region and
        locale.
        """

        super().__init__(cache, region)
        self.locale = locale
        self.printer = pprint.PrettyPrinter(indent=4)
        self.has_missed = False

    def raw_query(self, path: str, namespace: Namespace,
                  path_root: str = "data/wow",
                  should_print: bool = False) -> Optional[dict]:
        """ Build a query for the game-data API and return the result. """

        namespace_str = get_namespace_str(namespace, self.region)
        namespace_data = self.cache.get(namespace_str)
        full_path = "{}/{}".format(path_root, path)

        # return cached result if we alredy have it
        if self.static_has(path):
            QueryEngine.log.debug("cache hit for '%s'", full_path)
            if should_print:
                self.printer.pprint(namespace_data[full_path])
            return namespace_data[full_path]
        self.has_missed = True

        token_str = "BAD_TOKEN"
        token = self.get_token()
        if token is not None:
            token_str = token

        args = {"locale": self.locale.value,
                "access_token": token_str,
                "namespace": namespace_str}
        query_str = get_query_str(self.region, full_path)
        QueryEngine.log.debug("query: '%s'", query_str)
        req = requests.get(query_str, params=args)

        # make sure we got a valid response
        if req.status_code != requests.codes["ok"]:
            QueryEngine.log.error("error querying '%s': %d %s", full_path,
                                  req.status_code, req.text)
            return None

        # write the cached result
        namespace_data[full_path] = req.json()
        if should_print:
            self.printer.pprint(namespace_data[full_path])
        return namespace_data[full_path]

    def save(self) -> None:
        """ Write the cache based on current data. """

        if self.has_missed:
            self.cache.save()

    def static_has(self, path: str, path_root: str = "data/wow") -> bool:
        """
        Check if we've already cached a result for a given static query.
        """

        namespace_str = get_namespace_str(Namespace.Static, self.region)
        return "{}/{}".format(path_root, path) in self.cache.get(namespace_str)

    def static_query(self, path: str,
                     should_print: bool = False) -> Optional[dict]:
        """ Execute a query for static data. """

        return self.raw_query(path, Namespace.Static,
                              should_print=should_print)
