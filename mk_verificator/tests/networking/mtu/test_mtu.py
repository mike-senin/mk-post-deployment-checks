import pytest
from mk_verificator import utils


@pytest.mark.parametrize(
    "groups",
    utils.get_groups(utils.get_configuration(__file__))
)
def test_mtu(local_salt_client, groups):
    skipped_ifaces = ["bonding_masters", "lo"]
    TOTAL = {}
    failed_ifaces = {}

    gauges = utils.get_expected_mtu(__file__)

    network_info = local_salt_client.cmd(groups, 'cmd.run', ['sudo ls /sys/class/net/'])

    for node, ifaces_info in network_info.iteritems():
        if 'kvm' in node:
            kvm_info = local_salt_client.cmd(node, 'cmd.run',
                                             ["virsh list | grep jse2 | awk '{print $2}' | xargs -n1 virsh domiflist | "
                                              "grep -v br-pxe | grep br- | awk '{print $1}'"])
            ifaces_info = kvm_info.get(node)
        node_name = node.split('-')[0]
        node_ifaces = ifaces_info.split('\n')
        if node_name not in gauges:
            print "Node {} is not matching expected groups!".format(node)
        else:
            ifaces = {}
            for iface in node_ifaces:
                if iface in skipped_ifaces:
                    continue
                iface_mtu = local_salt_client.cmd(node, 'cmd.run',
                                                  ['cat /sys/class/net/{}/mtu'.format(iface)])
                ifaces[iface] = iface_mtu.get(node)
            TOTAL[node] = ifaces

    for node_ in TOTAL:
        ifaces = TOTAL.get(node_)
        node_name_ = node_.split('-')[0]

        for iface in ifaces:
            if node_name_ not in gauges:
                continue
            else:
                group = gauges.get(node_name_)
                gauge = group.get(iface)
                mtu = ifaces.get(iface)
                if iface not in gauges:
                    continue
                elif int(mtu) != int(gauge):
                    failed_ifaces[node_].append(iface)

    assert not failed_ifaces, "Nodes with iface mismatch: ".format(failed_ifaces)
