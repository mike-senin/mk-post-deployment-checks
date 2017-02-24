import sys
import salt.client as client
import texttable as tt

# USAGE (from cfg node): sudo python services_checker.py <mask>
# where <mask> is like ctl* or ntw*


def draw_table_version_conflicts(nodes, pkts_data):

    tab = tt.Texttable(max_width=240)
    header = ['Service name']
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


output = local.cmd(sys.argv[1], 'service.get_all')

if len(output.keys()) < 2:
    print("Nothing to compare - only 1 node")
    exit()

nodes = []
pkts_data = []
my_set = set()

for node in output:
    nodes.append(node)
    my_set.update(output[node])

for srv in my_set:
    row = []
    row.append(srv)
    for node in nodes:
        if srv in output[node]:
            row.append("+")
        else:
            row.append("No service")
    if row.count(row[1]) < len(nodes):
        pkts_data.append(row)
draw_table_version_conflicts(nodes, pkts_data)
