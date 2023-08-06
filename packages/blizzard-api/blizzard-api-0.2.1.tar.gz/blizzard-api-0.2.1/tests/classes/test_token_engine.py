
"""
vbinds - Tests for token retrieval.
"""

# built-in
import os

# internal
from tests.environment import get_new_cache

# module under test
from vbinds.classes.token_engine import TokenEngine
from vbinds.classes import ID_ENV_KEY, SECRET_ENV_KEY


def test_token_engine_basic():
    """
    Get a new token, then make sure that the cached token is used next time.
    """

    engine = TokenEngine(get_new_cache())
    assert engine.get_token() is not None
    assert engine.get_token() is not None
    engine.cache.clean()


def test_token_failures():
    """ Test some of the token-retrieval failure modes. """

    # bad identity and secret values
    engine = TokenEngine(get_new_cache())
    engine.set_credentials("bad_id", "bad_secret", False)
    assert engine.get_token() is None
    engine.cache.clean()

    good_id = os.environ[ID_ENV_KEY]
    good_secret = os.environ[SECRET_ENV_KEY]

    del os.environ[ID_ENV_KEY]
    del os.environ[SECRET_ENV_KEY]

    engine = TokenEngine(get_new_cache())
    assert engine.get_token() is None
    engine.cache.clean()

    os.environ[ID_ENV_KEY] = good_id
    os.environ[SECRET_ENV_KEY] = good_secret
