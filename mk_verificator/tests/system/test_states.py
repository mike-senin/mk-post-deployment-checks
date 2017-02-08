import pytest

def test_check_cluster_state(local_salt_client):
    output = local_salt_client.cmd('*', 'state.apply', ['alex_test'],  kwarg={'test': 'True'})
    for node in output:
        for values in output[node].values():
            if not values['result']:
                if 'The following packages' in values['comment']:
                    version = local_salt_client.cmd(node, 'lowpkg.list_pkgs')[node][values['name']]
                    assert values['result'], \
                    "Failed. Current version is {0}. {1}".format(version,(values['comment']))
                else:
                    assert values['result'], \
                    "Failed. Info: {}".format(values['comment'])
