import mk_verificator.utils.ssh_client as ssh
import pytest


def test_floating_ip(vm, floating_ip):
    vm.add_floating_ip(floating_ip)
    ssh_client = ssh.Node('vm', floating_ip.ip, 'cirros', 'cubswin:)')
    ssh_stdout = ssh_client.run('hostname')
    ssh_client.ping(floating_ip.ip)
    assert ssh_stdout == vm.name
