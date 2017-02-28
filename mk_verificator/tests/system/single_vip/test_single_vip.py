import pytest
from mk_verificator import utils


@pytest.mark.parametrize(
    "group",
    utils.get_groups(utils.get_configuration(__file__))
)
def test_single_vip(local_salt_client, group):
    local_salt_client.cmd(group, 'saltutil.sync_all')
    nodes_list = local_salt_client.cmd(group, 'grains.item', ['ipv4'])

    ipv4_list = []

    for node in nodes_list:
        ipv4_list.extend(nodes_list.get(node).get('ipv4'))

    ipv4_list.sort()
    ipv4_list = list(filter(lambda ip: ip != '127.0.0.1', ipv4_list))

    result = set([x for x in ipv4_list if ipv4_list.count(x) > 1])

    assert not result, "VIP IP duplicate found " \
                       "in group {}\n{}".format(group, result)
