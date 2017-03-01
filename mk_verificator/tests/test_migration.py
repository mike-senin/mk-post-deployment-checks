import mk_verificator.utils as utils
import mk_verificator.clients.nova as nova


def test_migration_for_all_nodes():
    config = utils.get_configuration(__file__)
    zone = config['availability_zone']
    mk_nova = nova.nova()
    list_hosts = [host.host for host in mk_nova.client.hosts.list(zone)]
    vm = mk_nova.create_vm('test_migration')
    mk_nova.wait_for_vm_status_is_active(vm.id)
    vm_host = mk_nova.client.servers.find(id=vm.id)

    # replacing the current host to last place
    list_hosts.remove(vm_host._info['OS-EXT-SRV-ATTR:host'])
    list_hosts.append(vm_host._info['OS-EXT-SRV-ATTR:host'])

    for host in list_hosts:
        vm.live_migrate(host=host)
        mk_nova.checking_vm_host(vm.id, host)
    vm.delete()
