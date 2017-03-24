import pytest
from mk_verificator import utils
from collections import Counter


@pytest.mark.parametrize(
    "group",
    utils.get_groups(utils.get_configuration(__file__))
)
def test_single_vip(local_salt_client, group):
    config = utils.get_configuration(__file__)

    local_salt_client.cmd(group, 'saltutil.sync_all')
    nodes_list = local_salt_client.cmd(group, 'grains.item',
                                       [config["protocol"]])

    ipv4_list = []

    for node in nodes_list:
        ipv4_list.extend(nodes_list.get(node).get(config["protocol"]))

    cnt = Counter(ipv4_list)

    for ip in cnt:
        if ip == config["host_ip"]:
            continue
        elif cnt[ip] > 1:
            assert "VIP IP duplicate found " \
                   "in group {}\n{}".format(group, ipv4_list)
