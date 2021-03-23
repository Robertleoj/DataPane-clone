import pytest

import datapane as dp
import datapane.client.config as c
from datapane.client.utils import InvalidTokenError

from .conftest import TEST_SERVER, TEST_TOKEN


def test_auth():
    """Test API-based auth"""
    TEST_ENV = "test_env"

    fp = c.get_config_file(TEST_ENV, reset=True)

    try:
        dp.init(config_env=TEST_ENV)

        # check the config env file is default
        assert fp.read_text() == c.get_default_config()

        with pytest.raises(InvalidTokenError):
            dp.ping()

        # login
        dp.login(token=TEST_TOKEN, server=TEST_SERVER, env=TEST_ENV, cli_login=False)
        assert "datapane-test" == dp.ping()
        # logout
        dp.logout(env=TEST_ENV)

        # check we've reset the config env file back to default
        assert fp.read_text() == c.get_default_config()

        with pytest.raises(InvalidTokenError):
            dp.ping()
    finally:
        if fp.exists():
            fp.unlink()
