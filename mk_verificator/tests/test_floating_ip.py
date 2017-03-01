import mk_verificator.utils.ssh_client as ssh
import mk_verificator.clients.nova as nova


def test_floating_ip():
    mk_nova = nova.nova()
    vm = mk_nova.create_vm('test-floating-ip')
    mk_nova.wait_for_vm_status_is_active(vm.id)

    floating_ip = mk_nova.client.floating_ips.create(
                      mk_nova.client.floating_ip_pools.list()[0].name)
    vm.add_floating_ip(floating_ip)

    ssh_client = ssh.Node('vm', floating_ip.ip, 'cirros', 'cubswin:)')
    ssh_stdout = ssh_client.run('hostname')
    ssh_client.ping(floating_ip.ip)
    assert ssh_stdout == 'test-floating-ip'

    vm.delete()
