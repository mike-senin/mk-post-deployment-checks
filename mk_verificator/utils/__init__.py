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
        if nodes[node_name] and node_name not in skipped_nodes
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

    test_groups = []
    groups_from_config = config.get('groups')
    # check if config.yaml contains `groups` key
    if groups_from_config is not None:
        invalid_groups = []
        for group in groups_from_config:
            # check if group name from config
            # is substring of one of the groups
            grp = [x for x in groups if group in x]
            if grp:
                test_groups.append(grp[0])
            else:
                invalid_groups.append(group)
        if invalid_groups:
            raise ValueError('Config file contains'
                             ' invalid groups name: {}'.format(invalid_groups))

    return test_groups if test_groups else groups


def get_configuration(path_to_test):
    test_folder = os.path.dirname(os.path.abspath(path_to_test))
    config_file = '/'.join([test_folder, "config.yaml"])
    config = yaml.load(open(config_file, 'r'))
    return config
