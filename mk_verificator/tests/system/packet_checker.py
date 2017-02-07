#!/usr/bin/env python
import salt.client as client
import texttable as tt

local = client.LocalClient()

pkgs_info = local.cmd('*', 'lowpkg.list_pkgs')
nodes = pkgs_info.keys()

mask_minor_pkgs = []

groups = {}

for node_name, node_pkgs in pkgs_info.items():
    group_name = node_name.split('-')[0]
    if not groups.has_key(group_name):
        groups[group_name] = [(node_name, node_pkgs)]
    else:
        groups[group_name].append((node_name, node_pkgs))

packets_to_skip = []


def draw_table_missed_packets(node_1_name, node_2_name, pkts_data):
    tab = tt.Texttable()
    header = ['Packet name', 'Packet version']
    tab.set_cols_align(['r', 'r'])
    tab.set_cols_width([40, 40])
    tab.header(header)
    for pkt_name, version in pkts_data:
        tab.add_row([pkt_name, version])
    s = tab.draw()
    print "Packets installed on %s, but not installed on %s" % (node_1_name, node_2_name)
    print s
    print 


def draw_table_version_conflicts(node_1_name, node_2_name, pkts_data):
    tab = tt.Texttable()
    header = ['Packet name',
              'Node {0} version'.format(node_1_name),
              'Node {0} version'.format(node_2_name)]
    tab.set_cols_align(['r', 'r', 'r'])
    tab.set_cols_width([40, 40, 40])
    tab.header(header)
    for pkt_name, ver_1, ver_2 in pkts_data:
        tab.add_row([pkt_name, ver_1, ver_2])
    s = tab.draw()
    print "Packets with different versions:"
    print s
    print 


for group_name, nodes in groups.items():
    print "-" * 140
    if len(nodes) > 1:

        print "Start verification for group %s" % group_name

        for node_i in nodes:
            for node_j in nodes:
                if node_i[0] == node_j[0]:
                    continue

                node_i_name, node_j_name = node_i[0], node_j[0]
                node_i_pkgs, node_j_pkgs = node_i[1], node_j[1]

                missed_packets, version_conflicts = [], []

                for pkg_name in node_i_pkgs:
                    if pkg_name in packets_to_skip:
                        continue

                    if node_j_pkgs.has_key(pkg_name):
                        i_packet_version = node_i_pkgs[pkg_name]
                        j_packet_version = node_j_pkgs[pkg_name]
                        if i_packet_version != j_packet_version:
                            version_conflicts.append((pkg_name, i_packet_version, j_packet_version))
                    else:
                        i_packet_version = node_i_pkgs[pkg_name]
                        missed_packets.append((pkg_name, i_packet_version))

                if missed_packets:
                    draw_table_missed_packets(node_i_name, node_j_name, missed_packets)

                if version_conflicts:
                    draw_table_version_conflicts(node_i_name, node_j_name, version_conflicts)
    
                if missed_packets or version_conflicts:
                    print "-" * 140

    else:
       print "Verification for group %s was skipped due to count of nodes less than 2" % group_name
    print "-" * 140


def test_packet_version_mismatch(local_salt_client):
    pass