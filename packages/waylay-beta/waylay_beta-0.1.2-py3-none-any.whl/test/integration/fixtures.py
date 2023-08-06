"""reusable test fixtures"""
import os
import pytest

from waylay import (
    ClientCredentials,
    WaylayClient
)
from waylay.auth import (
    WaylayTokenAuth
)


def get_test_env(key: str, default: str = None) -> str:
    test_var = os.getenv(key, default)
    if not test_var:
        raise AttributeError(f'{key} environment variable not configured, while test requires it.')
    return test_var


@pytest.fixture
def waylay_test_user_id():
    "environment variable WAYLAY_TEST_USER_ID"
    return get_test_env('WAYLAY_TEST_USER_ID')


@pytest.fixture
def waylay_test_user_secret():
    "environment variable WAYLAY_TEST_USER_SECRET"
    return get_test_env('WAYLAY_TEST_USER_SECRET')


@pytest.fixture
def waylay_test_accounts_url():
    "environment variable WAYLAY_TEST_ACCOUNTS_URL or 'https://accounts-api-staging.waylay.io'"
    return get_test_env('WAYLAY_TEST_ACCOUNTS_URL', 'https://accounts-api-staging.waylay.io')


@pytest.fixture
def waylay_test_client_credentials(waylay_test_user_id, waylay_test_user_secret, waylay_test_accounts_url):
    """
    client credentials as given in the environment variables
    WAYLAY_TEST_USER_ID, WAYLAY_TEST_USER_SECRET, WAYLAY_TEST_ACCOUNTS_URL
    """
    return ClientCredentials(
        waylay_test_user_id, waylay_test_user_secret, waylay_test_accounts_url
    )


@pytest.fixture
def waylay_test_token_string(waylay_test_client_credentials):
    token = WaylayTokenAuth(waylay_test_client_credentials).assure_valid_token()
    return token.token_string


@pytest.fixture
def waylay_test_client(waylay_test_client_credentials):
    waylay_client = WaylayClient.from_credentials(waylay_test_client_credentials)
    return waylay_client
