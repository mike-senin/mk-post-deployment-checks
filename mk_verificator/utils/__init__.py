import os
import yaml

import salt.client as client


def init_salt_client():
    local = client.LocalClient()
    return local


def get_active_nodes(config):
    local_salt_client = init_salt_client()

    skipped_nodes = config.get('skipped_nodes') or []
    # TODO add skipped nodes to cmd command instead of filtering
    nodes = local_salt_client.cmd('*', 'test.ping')
    active_nodes = [
        node_name for node_name in nodes
        if nodes[node_name] and not node_name in skipped_nodes
    ]
    return active_nodes


def get_groups(config):
    active_nodes = get_active_nodes(config)
    skipped_group = config.get('skipped_group') or []
    groups = []

    for node in active_nodes:
        group_name = "{group_name}*".format(
            group_name=node.split('-')[0]
        )
        if group_name not in skipped_group and group_name not in groups:
            groups.append(group_name)

    return groups


def get_configuration(path_to_test):
    test_folder = os.path.dirname(os.path.abspath(path_to_test))
    config_file = '/'.join([test_folder, "config.yaml"])
    config = yaml.load(open(config_file, 'r'))
    return config