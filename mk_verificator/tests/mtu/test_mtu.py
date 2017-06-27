import pytest
from mk_verificator import utils


@pytest.mark.parametrize(
    "group",
    utils.get_groups(utils.get_configuration(__file__))
)
def test_mtu(local_salt_client, group):
    config = utils.get_configuration(__file__)

    skipped_ifaces = config["skipped_ifaces"]
    expected_mtu = config["expected_mtu"]

    total = {}
    failed_ifaces = {}

    network_info = local_salt_client.cmd(
        group, 'cmd.run', ['sudo ls /sys/class/net/'], expr_form='pcre')

    kvm_nodes = local_salt_client.cmd(
        'salt:control', 'test.ping', expr_form='pillar').keys()

    for node, ifaces_info in network_info.iteritems():
        if node in kvm_nodes:
            kvm_info = local_salt_client.cmd(node, 'cmd.run',
                                             ["virsh list | grep jse2 | "
                                              "awk '{print $2}' | "
                                              "xargs -n1 virsh domiflist | "
                                              "grep -v br-pxe | grep br- | "
                                              "awk '{print $1}'"])
            ifaces_info = kvm_info.get(node)
        group_name = node.split('-')[0]
        node_ifaces = ifaces_info.split('\n')
        if group_name not in expected_mtu:
            continue
        else:
            ifaces = {}
            for iface in node_ifaces:
                if iface in skipped_ifaces:
                    continue
                iface_mtu = local_salt_client.cmd(node, 'cmd.run',
                                                  ['cat /sys/class/'
                                                   'net/{}/mtu'.format(iface)])
                ifaces[iface] = iface_mtu.get(node)
            total[node] = ifaces

    for node in total:
        ifaces = total.get(node)
        group_name = node.split('-')[0]

        for iface in ifaces:
            if group_name not in expected_mtu:
                continue
            else:
                group = expected_mtu.get(group_name)
                gauge = group.get(iface)
                mtu = ifaces.get(iface)
                if iface not in expected_mtu:
                    continue
                elif int(mtu) != int(gauge):
                    failed_ifaces[node].append(iface)

    assert not failed_ifaces, "Nodes with " \
                              "iface mismatch: {}".format(failed_ifaces)
