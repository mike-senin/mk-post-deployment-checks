#!/usr/bin/env python
# RUN AS SUDO ON SALT MASTER

import salt.client as client
import texttable as tt
import pdb

data_to_draw = {}
node_times_list = []
h = 0
m = 0
s = 0
h_gauge = 0
m_gauge = 0
s_gauge = 5


def count_avg_time(node_times_list):
    print "Counting AVG time..."
    global h, m, s
    divisor = 0
    for time_list in node_times_list:
        h += int(time_list[0])
        m += int(time_list[1])
        s += int(time_list[2])
        divisor += 1
    h = h/divisor
    m = m/divisor
    s = s/divisor
    print "Counted..."


def draw_results_table(data_to_draw):
    print "Trying to draw a table with the results..."
    global h, m, s, h_gauge, m_gauge, s_gauge

    tab = tt.Texttable()
    tab.set_chars(['-', '|', '+', '-'])
    tab.set_cols_align(["c", "c", "c", "c"])
    tab.set_cols_valign(["c", "c", "c", "c"])
    tab.add_row(["Node", "Time", "AVG time", "Result"])

    for node in data_to_draw:
        tab.add_row([node, "", "", ""])
        ntime = data_to_draw.get(node)

        n_time = "{}h {}m {}s".format(ntime[0],
                                      ntime[1],
                                      ntime[2])
        tgauge = "{}h {}m {}s".format(h, m, s)

        if (int(ntime[0]) - h) != h_gauge:
            tab.add_row(["",n_time, tgauge, "FAILED"])
        elif (int(ntime[1]) - m) != m_gauge:
            tab.add_row(["", n_time, tgauge, "FAILED"])
        elif (int(ntime[2]) - s) > s_gauge:
            # TODO: add correct verification for seconds difference
            tab.add_row(["", n_time, tgauge, "FAILED"])
        else:
            tab.add_row(["", n_time, tgauge, "+"])
    # TODO: draw only table with FAILED results
    print tab.draw()


def main():
    global nodes_info
    local = client.LocalClient()

    try:
        print "Trying to obtain nodes time..."
        nodes_info = local.cmd('ctl*', 'cmd.run', ['sudo date +"%H %M %S"'])
    except Exception as e:
        print e

    print "Filling up buffer with data..."
    for node, time in nodes_info.iteritems():
        node_times = time.split(' ')
        data_to_draw[node] = node_times
        node_times_list.append(node_times)

    count_avg_time(node_times_list)
    draw_results_table(data_to_draw)
    print "\nDONE"

if __name__ == "__main__":
    main()