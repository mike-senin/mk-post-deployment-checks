import pytest
import time
import mk_verificator.utils as utils
import mk_verificator.utils.ssh_client as ssh
# TODO
# Create fixture for adding/removing keypair
# Create fixture for checking security groups


@pytest.mark.parametrize(
    'count,block_size',
    [('4k', 262144), ('1M', 1024), ('1G', 1)]
)
def test_dd(vm_kp, floating_ip, request, global_results,
            count, block_size):
    config = utils.get_configuration(__file__)
    vm_kp.add_floating_ip(floating_ip)
    time.sleep(60)
    ssh_client = ssh.Node('vm', floating_ip.ip,
                          'ubuntu', pub_key=config['key_path'])
    ssh_client.run('rm test.dat')
    ssh_stdout = ssh_client.run('dd if=/dev/zero of=test.dat \
                                oflag=direct bs={0} count={1}'.
                                format(count, block_size))
    global_results.update(request.node.name,
                          ssh_stdout.split(" ")[-2] +
                          " " + ssh_stdout.split(" ")[-1])
