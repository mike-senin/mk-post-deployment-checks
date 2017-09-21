import pytest
import salt.client as client
import mk_verificator.utils as utils
import glanceclient.client as gl_client
from keystoneauth1.identity import v3
from keystoneauth1 import session


@pytest.fixture
def local_salt_client():
    local = client.LocalClient()
    return local


@pytest.fixture
def glance_client():
    config = utils.get_configuration(__file__)

    auth = v3.Password(
        auth_url=config['url_v3'],
        username=config['admin_username'],
        password=config['admin_password'],
        project_id=config['admin_project_id'],
        user_domain_id='default',
        project_domain_id='default')
    sess = session.Session(auth=auth, verify=False)

    endpoint = auth.get_endpoint(
        session=sess, service_type='image', interface='internal')
    client = gl_client.Client(
        config['glance_version'], endpoint, session=sess)

    return client
