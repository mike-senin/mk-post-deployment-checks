import pytest
import mk_verificator.utils as utils
import mk_verificator.clients.nova as nova


def test_migration_for_all_nodes(vm):
    config = utils.get_configuration(__file__)
    zone = config['availability_zone']
    mk_nova = nova.Nova()
    list_hosts = [host.host for host in mk_nova.client.hosts.list(zone)]

    # put current host at the end of the list
    list_hosts.remove(vm._info['OS-EXT-SRV-ATTR:host'])
    list_hosts.append(vm._info['OS-EXT-SRV-ATTR:host'])

    for host in list_hosts:
        vm.live_migrate(host=host)
        mk_nova.checking_vm_host(vm.id, host)
