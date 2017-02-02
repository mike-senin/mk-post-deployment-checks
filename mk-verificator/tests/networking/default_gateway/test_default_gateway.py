import json
import pytest


@pytest.mark.parametrize(
    ("group"), [
        'ceph*',
        'cmp*',
        'ctl*'
        'saml*'
        # TODO
    ])
def test_check_default_gateways(local_salt_client, group):

    netstat_info = \
        local_salt_client.cmd(group, 'cmd.run', ['ip r | sed -n 1p'])

    gateways =  {} # set(netstat_info.values())
    nodes = netstat_info.keys()
    for node in nodes:
        if not gateways.has_key(netstat_info[node]):
            gateways[netstat_info[node]] = [node]
        else:
            gateways[netstat_info[node]].append(node)

    assert len(gateways) != 1, json.dumps(gateways, indent=4)
