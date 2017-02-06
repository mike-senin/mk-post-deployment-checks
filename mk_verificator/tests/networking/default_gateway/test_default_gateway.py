import json
import pytest

from mk_verificator import utils


@pytest.mark.parametrize(
    ("group"),
    utils.get_groups(utils.get_configuration(__file__))
)
def test_check_default_gateways(local_salt_client, group):

    netstat_info = \
        local_salt_client.cmd(group, 'cmd.run', ['ip r | sed -n 1p'])

    gateways =  {}
    nodes = netstat_info.keys()

    for node in nodes:
        if not gateways.has_key(netstat_info[node]):
            gateways[netstat_info[node]] = [node]
        else:
            gateways[netstat_info[node]].append(node)

    assert len(gateways.keys()) == 1, \
        "There were found few gateways within group {group}: {gw}".format(
        group=group,
        gw=json.dumps(gateways, indent=4)
    )
