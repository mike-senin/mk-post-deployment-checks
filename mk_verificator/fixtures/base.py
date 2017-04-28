import pytest
import salt.client as client
import mk_verificator.utils as utils
import glanceclient.client as gl_client
from keystoneauth1.identity import v3
from keystoneauth1 import session
# TODO merge vm and vm_kp in one fixture


@pytest.fixture
def local_salt_client():
    local = client.LocalClient()
    return local


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
    groups = [
        node.split('-')[0] for node in active_nodes
        if node not in skipped_group
    ]
    return groups


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
