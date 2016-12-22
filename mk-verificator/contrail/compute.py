import salt.client as client

local = client.LocalClient()

def contrail_status():

    cs = local.cmd('cpu*', 'cmd.run', ['contrail-status | grep -Pv \'(==|^$)\''])
    broken_services = []
    for node in cs:
        for line in cs[node].split('\n'):
            line = line.strip()
            name, status = line.split(None, 1)
            if status not in {'active'}:
                err_msg = "{node}:{service} - {status}".format(
                    node=node, service=name, status=status)
                broken_services.append(err_msg)
    if broken_services:
        raise Exception('Broken services: {}'.format(broken_services))
    else:
        print 'Pass'


def main():
    contrail_status()

if __name__ == "__main__":
    main()

