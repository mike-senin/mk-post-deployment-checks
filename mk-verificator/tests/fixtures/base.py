import pytest
import salt.client as client


@pytest.fixture
def local_salt_client():
    local = client.LocalClient()
    return local

