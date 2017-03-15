import pytest
import mk_verificator.utils as utils


@pytest.fixture
def create_vm(nova_client):
    config = utils.get_configuration(__file__)

    image_id = config['image_ref']
    flavor_id = config['flavor_ref']

    net_id = config['network_ref']

    nics = [{"net-id": net_id, "v4-fixed-ip": ''}]
    vm = nova_client.servers.create(
        'test_migration', image_id, flavor_id, nics=nics)

    return vm


def checking_vm_host(client, vm_id, target_host):
    utils.wait_for_vm_status_is_active(client, vm_id)
    host = client.servers.find(id=vm_id)._info['OS-EXT-SRV-ATTR:host']

    assert host == target_host, "VM didn't migrate"


def test_migration_for_all_nodes(nova_client, create_vm):
    config = utils.get_configuration(__file__)
    zone = config['availability_zone']

    list_hosts = [host.host for host in nova_client.hosts.list(zone)]

    utils.wait_for_vm_status_is_active(nova_client, create_vm.id)

    vm_host = nova_client.servers.find(id=create_vm.id)

    # replacing the current host to last place
    list_hosts.remove(vm_host._info['OS-EXT-SRV-ATTR:host'])
    list_hosts.append(vm_host._info['OS-EXT-SRV-ATTR:host'])

    for host in list_hosts:
        create_vm.live_migrate(host=host)
        checking_vm_host(nova_client, create_vm.id, host)
    create_vm.delete()
