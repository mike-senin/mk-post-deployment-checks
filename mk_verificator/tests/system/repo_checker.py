#!/usr/bin/env python
import json
import salt.client as client

local = client.LocalClient()

name_node = '*'

print "Script checks difference between 'salt pillar.data linux:system:repo' and 'cat /etc/apt/sources.list.d/*; cat /etc/apt/sources.list'"
info = local.cmd(name_node, 'pillar.data', ['linux:system:repo'])
info_cat = local.cmd(name_node, 'cmd.run', ['cat /etc/apt/sources.list.d/*;cat /etc/apt/sources.list|grep deb'])

temp = {}
for node in info_cat:
    if not temp.has_key(node):
        l = []
        l.extend(info_cat[node].split('\n'))
        temp[node] = l
    else:
        temp[node].extend(info_cat[node].split('\n'))

    for index in range(len(temp[node])):
        temp[node][index] = temp[node][index].replace('/ ',' ')
info_cat = temp

temp = {}
for node in info:
    for repo in info[node]['linux:system:repo']:
        if not temp.has_key(node):
            temp[node] = [info[node]['linux:system:repo'][repo]['source'].replace('/ ', ' ')]
        else:
            temp[node].append(info[node]['linux:system:repo'][repo]['source'].replace('/ ', ' '))
info = temp

groups = {}
for node_name, node_gw in info.items():
    group_name = node_name.split('-')[0]
    if not groups.has_key(group_name):
        groups[group_name] = [node_name]
    else:
        groups[group_name].append(node_name)
    groups[group_name].sort()

for group_name, nodes in groups.items():
    for node in nodes:
        info[node].sort()
        info_cat[node].sort()
        if not info[node] == info_cat[node]:
            print json.dumps(node, indent=4)
            print '"salt pillar.data, linux:system:repo":'
            print json.dumps(info[node], indent=4)
            print '"cat /etc/apt/sources.list.d/*;cat /etc/apt/sources.list|grep deb":'
            print json.dumps(info_cat[node], indent=4)
        else:
            print node + ' > OK'
        #import pdb; pdb.set_trace()
