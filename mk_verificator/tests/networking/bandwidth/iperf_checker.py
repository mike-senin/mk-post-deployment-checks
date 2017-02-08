#!/usr/bin/env python
import salt.config as config
import salt.client as client
import texttable as tt


groups = {
    'ceph': {
        'private': 'eno1',
        'storage': 'storage',
        'control-plane': 'cp'
    },
    'cpu': {
        'private': 'eno1',
        'storage': 'bond0.1208',
        'control-plane': 'bond0.1204',
        'data': 'vhost0'
    },
    'ctl': {
        'private': 'eth0',
        'storage': 'eth2',
        'control-plane': 'eth1',
        'public': 'eth3'
    },
    'ntw': {
        'private': 'eth0',
        'control-plane': 'eth1',
        'data': 'eth2',
    },
    'nal': {
        'private': 'eth0',
        'control-plane': 'eth1',
    },
    'rmq': {
        'private': 'eth0',
        'control-plane': 'eth1',
    },
    'sql': {
        'private': 'eth0',
        'control-plane': 'eth1',
    },
    'prx': {
        'private': 'eth0',
        'control-plane': 'eth1',
        'public': 'eth2'
    },
    'mon': {
        'private': 'eth0',
        'control-plane': 'eth1',
        'data': 'eth2',
    },
    'mtr': {
        'private': 'eth0',
        'control-plane': 'eth1',
    },
    'log': {
        'private': 'eth0',
        'control-plane': 'eth1',
    },
    'asc': {
        'private': 'eth0',
        'control-plane': 'eth1',
    },
    'des': {
        'private': 'eth0',
        'control-plane': 'eth1',
    },
    'kvm': {
        'private': 'br-pxe',
        'control-plane': 'br-cp',
    },
    'saml': {
        'private': 'eth0',
        'control-plane': 'eth1',
        'public': 'eth2',
    }

}


master_client = client.LocalClient()

measurement_results = []
nodes = master_client.cmd('*', 'test.ping')
skipped_nodes = ['saml-global-01.mosci.jiocloud.com']
active_nodes = [
    node_name for node_name in nodes
    if nodes[node_name] and not node_name in skipped_nodes
]

# TODO delete
global_results = []


def draw_table_with_results():
    tab = tt.Texttable()
    header = [
        'nodes group',
        'sender node name',
        'reciever node name',
        'network',
        'bandwidth']
    tab.set_cols_align(['l', 'l', 'l', 'l', 'l'])
    tab.set_cols_width([5, 30, 30, 15, 30])
    tab.header(header)
    for row in global_results:
        tab.add_row(row)
    s = tab.draw()
    print s


def init_iperf_servers():
    master_client.run_job('*', 'cmd.run', ['iperf -s'])


def drop_iperf_servers():
    results = master_client.cmd_async('*', 'cmd.run', ['killall -9 iperf'])
    return results


def _get_ip_by_iface(minion_name, iface):
    ifaces = master_client.cmd(minion_name, 'network.ip_addrs', [iface])
    return ifaces.values()[0][0]


def _start_iperf_client(minion_name, target_ip, thread_count=None):
    # TODO (msenin) add thread param
    iperf_command = 'iperf -c {0}'.format(target_ip)
    if thread_count:
        iperf_command += ' -P {0}'.format(thread_count)
    result = master_client.cmd(minion_name, 'cmd.run', [iperf_command])
    return result


def _parse_iperf_results(minion_raw_output):
    iperf_results = minion_raw_output.values()[0]
    try:
        results = iperf_results.split('\n')[-1][7:]
    except Exception:
        results = str(iperf_results)
    return results


def _add_to_global_table(
        nodes_group,
        sender_node_name,
        reciever_node_name,
        network,
        bandwidth):
    global_results.append([nodes_group, sender_node_name,
                           reciever_node_name, network, bandwidth])


def _prepare_network_info(group_name_i, group_name_j):
    if not (group_name_i in groups and group_name_j in groups):
        print "Test skipped for groups: {0} and {1}".format(group_name_i, group_name_j)
        return

    available_networks_for_pair = \
        set(groups[group_name_i].keys()) & set(groups[group_name_j].keys())
    network_data = {}
    for network in available_networks_for_pair:
        iface_sender = groups[group_name_i][network]
        iface_reciever = groups[group_name_j][network]
        # TODO (msenin) expected speed
        expected_speed = 1
        network_data[network] = \
            (iface_sender, iface_reciever, expected_speed)
    return network_data


def _start_iperf_between_hosts(node_i, node_j):
    group_name_i = node_i.split('-')[0]
    group_name_j = node_j.split('-')[0]
    group_name = '{0}-{1}'.format(group_name_i, group_name_j)
    net_info = _prepare_network_info(group_name_i, group_name_j)

    for net_name in net_info:
        ifaces_info = net_info[net_name]
        local_iface, destination_iface, expected_speed = ifaces_info
        try:
            local_ip = _get_ip_by_iface(node_i, local_iface)
        except:
            print node_i, local_iface

        try:
            destination_ip = _get_ip_by_iface(node_j, destination_iface)
        except:
            print node_j, destination_iface

        direct_raw_results = _start_iperf_client(node_i, destination_ip)
        direct_results = _parse_iperf_results(direct_raw_results)

        _add_to_global_table(group_name,
                             node_i, node_j, net_name, direct_results)

        reverse_raw_results = _start_iperf_client(node_j, local_ip)
        reverse_results = _parse_iperf_results(reverse_raw_results)

        _add_to_global_table(group_name,
                             node_j, node_i, net_name, reverse_results)


def start_network_measurements():
    for _i in xrange(len(active_nodes)):
        for _j in xrange(len(active_nodes)):
            if _i < _j:
                node_i = active_nodes[_i]
                node_j = active_nodes[_j]
                try:
                    print "Start measurement between {} and {}".format(node_i, node_j)
                    _start_iperf_between_hosts(node_i, node_j)
                    print "Measurement between {} and {} have been finished".format(node_i, node_j)
                except Exception as e:
                    print "Failed for {0} {1}".format(node_i, node_j)
                    print e
    return


if __name__ == '__main__':
    init_iperf_servers()
    try:
        start_network_measurements()
    except Exception as e:
        print "Some errors were occured during measurements:"
        print e
    drop_iperf_servers()
    draw_table_with_results()
