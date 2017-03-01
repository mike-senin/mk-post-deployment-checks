<<<<<<< HEAD
=======
import pytest
import salt.client as client
import novaclient.client as nv_client
import glanceclient.client as gl_client
import mk_verificator.utils as utils
from keystoneauth1 import loading, session


@pytest.fixture
def local_salt_client():
    local = client.LocalClient()
    return local


@pytest.fixture
def nova_client():
    config = utils.get_configuration(__file__)

    # TODO(den) openstack catalog list
    version = '2.1'

    client = nv_client.Client(
        version,
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

    loader = loading.get_plugin_loader('password')
    auth = loader.load_from_options(
        auth_url=config['url'],
        username=config['admin_username'],
        password=config['admin_password'],
        project_id=config['admin_project_id'])
    session = session.Session(auth=auth)

    # TODO(den) openstack catalog list
    version = '2'

    client = gl_client.Client(version, session=session)
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
