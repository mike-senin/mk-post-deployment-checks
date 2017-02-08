#!/usr/bin/env python
# RUN AS SUDO ON SALT MASTER
# TODO: optionally use args to have a list of MTU for specific node set

import salt.client as client
import texttable as tt


expectations = {
    "ceph": {
        "bond0": "9100",
        "bond0.1204": "9100",
        "bond0.1208": "9100",
        "cp": "9100",
        "eno4": "9100",
        "ens2f0": "9100",
        "ens2f1": "9100",
        "storage": "9100"
    },
    "kvm": {
        "bond0": "9100",
        "bond0.1201": "9100",
        "bond0.1202": "9100",
        "bond0.1204": "9100",
        "bond0.1208": "9100",
        "br-cp": "9100",
        "br-private": "9100",
        "br-public": "9100",
        "br-pxe": "1500",
        "br-storage": "9100",
        "eno3": "9100",
        "eno4": "9100",
        "vnet0": "9100",
        "vnet1": "9100",
        "vnet2": "9100",
        "vnet3": "9100",
        "vnet4": "9100",
        "vnet5": "9100",
        "vnet6": "9100",
        "vnet7": "9100",
        "vnet8": "9100",
        "vnet9": "9100",
        "vnet10": "9100",
        "vnet11": "9100",
        "vnet12": "9100",
        "vnet13": "9100",
        "vnet14": "9100",
        "vnet15": "9100",
        "vnet16": "9100",
        "vnet17": "9100",
        "vnet18": "9100",
        "vnet19": "9100",
        "vnet20": "9100",
        "vnet21": "9100",
        "em3": "9100",
        "em4": "9100"
    },
    "prx": {
        "eth0": "1500",
        "eth1": "9000",
        "eth2": "9000"
    },
    "cpu": {
        "bond0": "9100",
        "bond0.1202": "9100",
        "bond0.1204": "9100",
        "bond0.1208": "9100",
        "bonding_masters": "9000",
        "eno3": "9100",
        "eno4": "9100",
        "tap09bdf181-45": "9000",
        "tap8a299d2d-5d": "9000",
        "vhost0": "9100"
    },
    "rmq": {
        "eth0": "1500",
        "eth1": "9000"
    },
    "sql": {
        "eth0": "1500",
        "eth1": "9000"
    },
    "ctl": {
        "eth0": "1500",
        "eth1": "9000",
        "eth2": "9000",
        "eth3": "9000"
    },
    "des": {
        "eth0": "1500",
        "eth1": "9000"
    },
    "nal": {
        "eth0": "1500",
        "eth1": "9000"
    },
    "saml": {
        "eth0": "1500",
        "eth1": "9000",
        "eth2": "9000"
    },
    "asc": {
        "eth0": "1500",
        "eth1": "9000"
    },
    "ntw": {
        "eth0": "1500",
        "eth1": "9000",
        "eth2": "9000"
    },
    "apt": {
        "eth0": "1500"
    },
    "log": {
        "eth0": "1500",
        "eth1": "9000"
    },
    "mtr": {
        "eth0": "1500",
        "eth1": "9000"
    },
    "mon": {
        "eth0": "1500",
        "eth1": "9000"
    }
}

TOTAL = {}
network_info = {}
node_ifaces = {}
# TODO add func that works with iface_names
# and collects info from them but not from all nodes
iface_names = ("ceph", "kvm", "prx",
               "cpu", "rmq", "sql",
               "ctl", "des", "nal",
               "saml", "asc", "ntw",
               "apt", "log", "mtr",
               "mon")


def get_node_ifaces_info(node_, node_ifaces_, local):
    skipped_ifaces = ["bonding_masters", "lo"]
    print "Trying to gather ifaces info for {}...".format(node_)
    ifaces = {}
    for iface in node_ifaces_:
        if iface in skipped_ifaces:
            continue
        try:
            iface_mtu = local.cmd(node_, 'cmd.run',
                                  ['cat /sys/class/net/{}/mtu'.format(iface)])
            ifaces[iface] = iface_mtu.get(node_)
        except Exception as e_:
            print e_
    TOTAL[node_] = ifaces


def draw_results_table(total):
    # TODO: add vidth for 1st column with node name
    print "Trying to draw a table with the results..."

    failed_tab = tt.Texttable()
    failed_tab.set_chars(['-', '|', '+', '-'])
    failed_tab.set_cols_align(["c", "c", "c", "c", "c"])
    failed_tab.set_cols_valign(["c", "c", "c", "c", "c"])
    failed_tab.set_cols_width([26, 7, 10, 10, 10])
    failed_tab.add_row(["Node", "Iface", "MTU set", "MTU expected", "Result"])

    for node_ in total:
        ifaces = total.get(node_)
        node_name_ = node_.split('-')[0]
        failed_tab.add_row([node_, "", "", "", ""])
        for iface in ifaces:
            if node_name_ not in expectations:
                continue
            else:
                group = expectations.get(node_name_)
                gauge = group.get(iface)
                mtu = ifaces.get(iface)
                if iface not in expectations:
                    continue
                elif int(mtu) != int(gauge):
                    failed_tab.add_row(["", iface, mtu, gauge, "FAILED"])
    print "Failed MTU interfaces:"
    print failed_tab.draw()


def main():
    global network_info, node_ifaces
    local = client.LocalClient()

    try:
        print "Trying to obtain nodes with interfaces..."
        network_info = local.cmd('*', 'cmd.run', ['sudo ls /sys/class/net/'])
    except Exception as e:
        print e

    for node, ifaces_info in network_info.iteritems():
        try:
            if 'kvm' in node:
                kvm_info = local.cmd(
                    node, 'cmd.run', [
                        "virsh list | grep jse2 | awk '{print $2}' | xargs -n1 virsh domiflist | "
                        "grep -v br-pxe | grep br- | awk '{print $1}'"])
                ifaces_info = kvm_info.get(node)
            node_name = node.split('-')[0]
            node_ifaces = ifaces_info.split('\n')
            if node_name not in expectations:
                print "Node {} is not matching expected groups!".format(node)
            else:
                try:
                    get_node_ifaces_info(node, node_ifaces, local)
                except Exception as e:
                    print e
        except Exception as e:
            print e

    draw_results_table(TOTAL)
    print "\nDONE"

if __name__ == "__main__":
    main()
