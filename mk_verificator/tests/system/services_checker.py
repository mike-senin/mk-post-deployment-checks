#!/usr/bin/env python
import salt.client as client
import texttable as tt

local = client.LocalClient()

pkgs_info = local.cmd('*', 'service.get_all')
nodes = pkgs_info.keys()

groups = {}

for node_name, node_services in pkgs_info.items():
    group_name = node_name.split('-')[0]
    if group_name not in groups:
        groups[group_name] = []
    else:
        groups[group_name].append((node_name, node_services))

services_to_skip = []


def draw_table_missed_services(node_1_name, node_2_name, services_data):
    tab = tt.Texttable()
    header = ['Service name']
    tab.set_cols_align(['r'])
    tab.set_cols_width([40])
    tab.header(header)
    for service_name in services_data:
        tab.add_row([service_name])
    s = tab.draw()
    print "Service installed on %s, but not installed on %s" % (
        node_1_name, node_2_name
    )
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
                node_i_services, node_j_services = node_i[1], node_j[1]

                missed_services = []

                for service_name in node_i_services:
                    if service_name in services_to_skip:
                        continue

                    if service_name not in node_j_services:
                        missed_services.append((service_name))

                if missed_services:
                    draw_table_missed_services(
                        node_i_name, node_j_name, missed_services)
                    print "-" * 140

    else:
        print "Verification for group {} was skipped "\
              "due to count of nodes less than 2".format(group_name)
    print "-" * 140
