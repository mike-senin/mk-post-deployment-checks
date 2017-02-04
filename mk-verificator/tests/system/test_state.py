#!/usr/bin/env python
import salt.client as client

local = client.LocalClient()

output = local.cmd('*', 'state.apply', ['alex_test'],  kwarg={'test': 'True'})
for node in output:
    print "Result for {}".format(node)
    for values in pkgs_info[node].values():
        if values['result']:
            print "Passed"
        else:
            if 'The following packages' in values['comment']:
                version = local.cmd(node, 'lowpkg.list_pkgs')[node][values['name']]
                print "Failed. Current version is {0}. {1}".format(version,(values['comment']))
            else:
                print "Failed. Info: {}".format(values['comment'])
