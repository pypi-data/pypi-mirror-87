import os

from tktl.core.clients.arrow import ArrowFlightClient
from tktl.core.managers.auth import AuthConfigManager


def test_instantiate_client():

    key = os.environ["TEST_USER_API_KEY"]
    AuthConfigManager.set_api_key(key)

    client = ArrowFlightClient(
        api_key=key, repository_name=f"{os.environ['TEST_USER']}/test-new"
    )
    assert client.location is None
