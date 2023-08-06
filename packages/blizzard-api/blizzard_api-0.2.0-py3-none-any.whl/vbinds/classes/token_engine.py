
"""
vbinds - A class for managing Blizzard API access tokens acquired from
         application identity and secret pairs.
"""

# built-in
import logging
import os
from typing import Optional

# third-party
import requests

# internal
from vbinds.enums import Region
from . import ID_ENV_KEY, SECRET_ENV_KEY
from .cache import Cache


class TokenEngine:
    """ A class for obtaining API-access tokens from Blizzard. """

    log = logging.getLogger(__name__)
    token_server = "https://{}.battle.net/oauth/token"

    def __init__(self, cache: Cache, region: Region = Region.US):
        """
        Construct a new token-engine from a cache and for a given region.
        """

        self.cache = cache
        self.region = region

    def get_token(self) -> Optional[str]:
        """
        Get a String access-token for the API or return None if this failed.
        """

        cred_data = self.get_credentials()
        if cred_data is None:
            return None

        # use cached token if it's already there
        if "token" in cred_data:
            token = cred_data["token"]["access_token"]
            TokenEngine.log.debug("using cached token '%s'", token)
            return token

        # get a new token
        req = requests.post(TokenEngine.token_server.format(self.region.value),
                            data={"grant_type": "client_credentials"},
                            auth=(cred_data["id"], cred_data["secret"]))

        # make sure we got a valid response
        if req.status_code != requests.codes["ok"]:
            TokenEngine.log.error("error getting new token: %s", req.json())
            return None

        # save the new token
        token_data = req.json()
        cred_data["token"] = token_data

        # return the new token
        token = cred_data["token"]["access_token"]
        TokenEngine.log.debug("got new token '%s'", token)
        return token

    def get_credentials(self) -> Optional[dict]:
        """
        Get the client-id and secret parameters required for obtaining a new
        token.
        """

        cred_data = self.cache.get("creds")

        # try to load (and set) credentials if we don't have them
        if "id" not in cred_data or "secret" not in cred_data:
            if (ID_ENV_KEY not in os.environ or
                    SECRET_ENV_KEY not in os.environ):
                err_msg = ("Couldn't load identity and secret from " +
                           "environment variables '%s' and '%s'")
                TokenEngine.log.error(err_msg, ID_ENV_KEY, SECRET_ENV_KEY)
                return None
            self.set_credentials(os.environ[ID_ENV_KEY],
                                 os.environ[SECRET_ENV_KEY])
            cred_data = self.cache.get("creds")

        return cred_data

    def set_credentials(self, client_id, client_secret,
                        write_cache: bool = True):
        """
        Set new credentials' data and optionally write-through to the cache.
        """

        cred_data = self.cache.get("creds")
        cred_data["id"] = client_id
        cred_data["secret"] = client_secret
        if write_cache:
            self.cache.save()
