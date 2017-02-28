import os
import yaml
import time

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
    """function returns configuration for environment

    and for test if it's specified"""
    global_config_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "../global_config.yaml")
    with open(global_config_file, 'r') as file:
        global_config = yaml.load(file)

    config_file = os.path.join(
        os.path.dirname(os.path.abspath(path_to_test)), "config.yaml")

    if os.path.exists(config_file):
        with open(config_file, 'r') as file:
            global_config.update(yaml.load(file))

    return global_config


def wait_for_vm_status_is_active(client, vm_id, retry_delay=5, timeout=60):
    timeout_reached = False
    start_time = time.time()
    while not timeout_reached:
        vm_status = client.servers.find(id=vm_id).status

        if vm_status == 'ACTIVE':
            break
        elif vm_status == 'ERROR':
            raise AssertionError("VM is in the status 'error'")

        time.sleep(retry_delay)
        timeout_reached = (time.time() - start_time) > timeout
    else:
        raise AssertionError("VM didn\'t get status active, "
                             "VM has '{}' status".format(vm_status))
