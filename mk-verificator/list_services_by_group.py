#!/usr/bin/env python
import salt.client as client
import texttable as tt

local = client.LocalClient()

services_info = local.cmd('*', 'service.get_all')
nodes = services_info.keys()

groups = {}

system_services = [
"acpid",
"apparmor",
"apport",
"atd",
"console-setup",
"cron",
"dbus",
"dns-clean",
"friendly-recovery",
"grub-common",
"irqbalance",
"killprocs",
"kmod",
"networking",
"ntp",
"ondemand",
"pppd-dns",
"procps",
"rc.local",
"resolvconf",
"rsync",
"rsyslog",
"screen-cleanup",
"sendsigs",
"ssh",
"sudo",
"udev",
"umountfs",
"umountnfs.sh",
"umountroot",
"unattended-upgrades",
"urandom",
]

def draw_services_table(services_data):
    tab = tt.Texttable()
    header = ['Service name']
    tab.set_cols_align(['r'])
    tab.set_cols_width([40])
    tab.header(header)
    for service_name in services_data:
        tab.add_row([service_name])
    s = tab.draw()

    print
    print s
    print

for node_name, node_services in services_info.items():
    group_name = node_name.split('-')[0]
    if not groups.has_key(group_name):
        groups[group_name] = set()
    else:
        for node_service in node_services:
            if node_service not in system_services:
                groups[group_name].add(node_service)


for group_name, services in groups.items():
    print "-" * 140
    print
    print "List of services for group %s" % group_name

    draw_services_table(services)

    print "-" * 140
