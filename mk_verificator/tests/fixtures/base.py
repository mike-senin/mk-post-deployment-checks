<<<<<<< HEAD
=======
import pytest
import salt.client as client
import novaclient.client as nv_client
import glanceclient.client as gl_client
import mk_verificator.utils as utils
from keystoneauth1.identity import v3
from keystoneauth1 import session


@pytest.fixture
def local_salt_client():
    local = client.LocalClient()
    return local


@pytest.fixture
def nova_client():
    config = utils.get_configuration(__file__)

    client = nv_client.Client(
        config['nova_version'],
        config['admin_username'],
        config['admin_password'],
        config['admin_project_id'],
        config['url'],
        service_type="compute",
        endpoint_type=config['endpoint_type'])
    return client


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

    client = gl_client.Client(config['glance_version'], session=sess)
    return client


@pytest.fixture
def active_nodes(local_salt_client, skipped_nodes=None):
    skipped_nodes = skipped_nodes or []
    nodes = local_salt_client.cmd('*', 'test.ping')
    active_nodes = [
        node_name for node_name in nodes
        if nodes[node_name] and node_name not in skipped_nodes
    ]
    return active_nodes


@pytest.fixture
def groups(active_nodes, skipped_group=None):
    skipped_group = skipped_group or []
    import pdb
    pdb.set_trace()
    groups = [
        node.split('-')[0] for node in active_nodes
        if node not in skipped_group
    ]
    return groups
>>>>>>> fixed glance client
