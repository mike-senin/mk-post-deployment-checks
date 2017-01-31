#!/usr/bin/env python

import json
import salt.client as client

def main():
    local = client.LocalClient()
    
    netstat_info = local.cmd('*', 'cmd.run', ['ip r | sed -n 1p'])
    # {node:"default via 10.xxx.xxx.xxx dev ethx", }

    groups = {}
    for node_name, node_gw in netstat_info.items():
        group_name = node_name.split('-')[0]
        if not groups.has_key(group_name):
            groups[group_name] = [node_name]
        else:
            groups[group_name].append(node_name)

    for group_name, nodes in groups.items():
        gw = {}
        for node in nodes:
            if not gw.has_key(netstat_info[node]):
                gw[netstat_info[node]] = [node]
            else:
                gw[netstat_info[node]].append(node)

        if len(gw) != 1:
            print '-' * 40
            print 'Gpoup: ' + group_name
            print json.dumps(gw, indent=4)

if __name__ == "__main__":
    main()
