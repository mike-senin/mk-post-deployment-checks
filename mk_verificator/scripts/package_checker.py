import sys
import salt.client as client
import texttable as tt

# USAGE (from cfg node): sudo python package_checker.py <mask>
# where <mask> is like ctl* or ntw*


def draw_table_version_conflicts(nodes, pkts_data):

    tab = tt.Texttable(max_width=240)
    header = ['Packet name']
    align = ['r']
    for node in nodes:
        header.append(node.split(".")[0])
        align.append('r')
    tab.set_cols_align(align)
    tab.header(header)
    for row in pkts_data:
        tab.add_row(row)
    s = tab.draw()
    print "Summary:"
    print s


local = client.LocalClient()


output = local.cmd(sys.argv[1], 'lowpkg.list_pkgs')

if len(output.keys()) < 2:
    print("Nothing to compare - only 1 node")
    exit()

nodes = []
pkts_data = []
my_set = set()

for node in output:
    nodes.append(node)
    my_set.update(output[node].keys())

for deb in my_set:
    row = []
    row.append(deb)
    for node in nodes:
        if deb in output[node].keys():
            row.append(output[node][deb])
        else:
            row.append("No package")
    if row.count(row[1]) < len(nodes):
        pkts_data.append(row)
draw_table_version_conflicts(nodes, pkts_data)

######################

pre_check = local.cmd(sys.argv[1], 'cmd.run', ['dpkg -l | grep "python-pip "'])

if pre_check.values().count('') > 0:
    print ("pip is not installed on one or more nodes. exiting")
    exit()

output = local.cmd(sys.argv[1], 'pip.freeze')

nodes = []
pkts_data = []
my_set = set()

for node in output:
    nodes.append(node)
    my_set.update([x.split("=")[0] for x in output[node]])
    output[node] = dict([x.split("==") for x in output[node]])

for deb in my_set:
    row = []
    row.append(deb)
    for node in nodes:
        if deb in output[node].keys():
            row.append(output[node][deb])
        else:
            row.append("No module")
    if row.count(row[1]) < len(nodes):
        pkts_data.append(row)
draw_table_version_conflicts(nodes, pkts_data)
