#!/usr/bin/env python
import salt.client as client
import texttable as tt
import itertools
from netaddr import IPNetwork, IPAddress

# ==========CONFIGURATION PART==========#
# Define network types their CIDR to be tested
nets = {"public": "192.0.0.0/24",
        "private": "192.0.1.0/24"}

# Define nodes to be tested (all pairs will be calculated)
# you can specify node types like this
# target_nodes=['ctl*','des*','asc*']
# you can choose some particular nodes (pay attention to format)
target_nodes = ['des-01.*', 'asc-01.*']
# you can even skip nodes from the list (not implemented yet)
# skipped_nodes = ['cpu-035.jpe1.jiocloud.com']
# you can define regex by your own (perl-type regex, -E option in salt)
nodes_regex = ''
# tbd maybe define networks for each node
# groups = {'ctl*': ['public'],'asc*': ['public','private']}
# ==========CONFIGURATION PART==========#
if not nodes_regex:
    nodes_regex = '({0})'.format("|".join(target_nodes))

master_client = client.LocalClient()
measurement_results = []

print master_client.cmd(expr_form='pcre', tgt=nodes_regex,
                        fun='cmd.run', arg=['apt-get install iperf'])
nodes = master_client.cmd(expr_form='pcre', tgt=nodes_regex,
                          fun='network.interfaces')
pairs = list(itertools.combinations(nodes.keys(), 2))

print "Ok, pairs are:"
print pairs
print "Ok, regex is:"
print nodes_regex

# TODO implement skip nodes and check if we have dead ones

# print nodes
# active_nodes = [
#    node_name for node_name in nodes
#    if nodes[node_name] and
#       node_name not in skipped_nodes and
#       "[Not connected]" not in nodes[node_name]
# ]
# print active_nodes

global_results = []


def draw_table_with_results():
    tab = tt.Texttable()
    header = [
        'node name 1',
        'node name 2',
        'network',
        'bandwidth >',
        'bandwidth <',
    ]
    tab.set_cols_align(['l', 'l', 'l', 'l', 'l'])
    tab.set_cols_width([27, 27, 15, 20, '20'])
    tab.header(header)
    for row in global_results:
        tab.add_row(row)
    s = tab.draw()
    print s


def init_iperf_servers():
    print master_client.run_job(expr_form='pcre', tgt=nodes_regex,
                                fun='cmd.run', arg=['iperf -s'])


def drop_iperf_servers():
    results = \
        master_client.cmd_async(expr_form='pcre', tgt=nodes_regex,
                                fun='cmd.run', arg=['killall -9 iperf'])
    return results


def _start_iperf_client(minion_name, target_ip, thread_count=None):
    # TODO (msenin) add thread param
    iperf_command = 'iperf -c {0}'.format(target_ip)
    if thread_count:
        iperf_command += ' -P {0}'.format(thread_count)
    result = master_client.cmd(minion_name, 'cmd.run', [iperf_command])
    return result


def _parse_iperf_results(raw_output):
    iperf_results = raw_output.values()[0].split('\n')[-1].split(' ')[-2:]
    try:
        results = ' '.join(iperf_results)
    except Exception:
        results = str(iperf_results)
    return results


def _add_to_global_table(
        sender_node_name,
        reciever_node_name,
        network,
        forward,
        backward):
    global_results.append([sender_node_name, reciever_node_name,
                           network, forward, backward])


def _start_iperf_between_hosts(node_i, node_j, ip_i, ip_j, net_name):
        direct_raw_results = _start_iperf_client(node_i, ip_j)
        forward = "1 thread:\n"
        forward += _parse_iperf_results(direct_raw_results)

        direct_raw_results = _start_iperf_client(node_i, ip_j, 10)
        forward += "\n\n10 thread:\n"
        forward += _parse_iperf_results(direct_raw_results)

        reverse_raw_results = _start_iperf_client(node_j, ip_i)
        backward = "1 thread:\n"
        backward += _parse_iperf_results(reverse_raw_results)

        reverse_raw_results = _start_iperf_client(node_j, ip_i, 10)
        backward += "\n\n10 thread:\n"
        backward += _parse_iperf_results(reverse_raw_results)
        _add_to_global_table(node_i, node_j, net_name, forward, backward)


def start_network_measurements():
    for net in nets:
        for pair in pairs:
            for interf in nodes[pair[0]]:
                # need to handle vips here
                ip = nodes[pair[0]][interf]['inet'][0]['address']
                # non_vip = nodes[pair[0]][interf]['inet'][0]['broadcast']
                if IPAddress(ip) in IPNetwork(nets[net]):
                    # print "FIRST IP is {}".format(ip)
                    for interf2 in nodes[pair[1]]:
                        if 'inet' not in nodes[pair[1]][interf2].keys():
                            continue
                        ip2 = nodes[pair[1]][interf2]['inet'][0]['address']
                        if IPAddress(ip2) in IPNetwork(nets[net]):
                            print "Will IPERF between {0} and {1}".format(ip,
                                                                          ip2)
                            try:
                                _start_iperf_between_hosts(pair[0], pair[1],
                                                           ip, ip2, net)
                                print "Measurement between {} and {} " \
                                      "has been finished".format(pair[0],
                                                                 pair[1])
                            except Exception as e:
                                print "Failed for {0} {1}".format(
                                      pair[0], pair[1])
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
