import pytest
import salt.client as client


@pytest.fixture
def local_salt_client():
    local = client.LocalClient()
    return local


@pytest.fixture()
def active_nodes(local_salt_client, skipped_nodes=None):
    skipped_nodes = skipped_nodes or []
    nodes = local_salt_client.cmd('*', 'test.ping')
    active_nodes = [
        node_name for node_name in nodes
        if nodes[node_name] and not node_name in skipped_nodes
    ]
    return active_nodes


@pytest.fixture()
def groups(active_nodes, skipped_group=None):
    skipped_group = skipped_group or []
    import pdb; pdb.set_trace()
    groups = [
        node.split('-')[0] for node in active_nodes
        if node not in skipped_group
    ]
    return groups