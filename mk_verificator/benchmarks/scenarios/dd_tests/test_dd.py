import pytest
import random
import time
import mk_verificator.clients.nova as nova
import mk_verificator.utils as utils
import mk_verificator.utils.ssh_client as ssh
# TODO
# Create fixture for adding/removing keypair
# Create fixture for checking security groups
# Try to reuse fixtures from tests folder


@pytest.yield_fixture(scope='module')
def vm():
    config = utils.get_configuration(__file__)
    mk_nova = nova.Nova()
    vm = mk_nova.create_vm(name='qa-framework-{}'.
                           format(random.randint(1, 100)),
                           key_name=config['key_name'])
    mk_nova.wait_for_vm_status_is_active(vm.id)
    yield vm
    vm.delete()


@pytest.yield_fixture(scope="module")
def floating_ip():
    mk_nova = nova.Nova()
    floating_ip = mk_nova.client.floating_ips.create(
                      mk_nova.client.floating_ip_pools.list()[0].name)
    yield floating_ip
    mk_nova.client.floating_ips.delete(floating_ip.id)


@pytest.mark.parametrize(
    'count,block_size',
    [('4k', 262144), ('1M', 1024), ('1G', 1)]
)
def test_dd(vm, floating_ip, request, global_results,
            count, block_size):
    config = utils.get_configuration(__file__)
    vm.add_floating_ip(floating_ip)
    time.sleep(60)
    ssh_client = ssh.Node('vm', floating_ip.ip,
                          'ubuntu', pub_key=config['key_path'])
    ssh_client.run('rm test.dat')
    ssh_stdout = ssh_client.run('dd if=/dev/zero of=test.dat \
                                oflag=direct bs={0} count={1}'.
                                format(count, block_size))
    global_results.update(request.node.name,
                          ssh_stdout.split(" ")[-2] +
                          " "+ssh_stdout.split(" ")[-1])
