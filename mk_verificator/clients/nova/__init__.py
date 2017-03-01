import novaclient.client as nv_client
import mk_verificator.utils as utils
import time


class nova():

    def __init__(self):
        config = utils.get_configuration(__file__)

        # TODO(den) openstack catalog list
        version = '2.1'

        client = nv_client.Client(
            version,
            config['admin_username'],
            config['admin_password'],
            config['admin_project_id'],
            config['url'],
            service_type="compute",
            endpoint_type=config['endpoint_type'])
        self.client = client

    def create_vm(self, name):
        config = utils.get_configuration(__file__)

        image_id = config['image_ref']
        flavor_id = config['flavor_ref']
        net_id = config['network_ref']
        nics = [{"net-id": net_id, "v4-fixed-ip": ''}]

        vm = self.client.servers.create(
            name, image_id, flavor_id, nics=nics)

        return vm

    def checking_vm_host(self, vm_id, target_host):
        self.wait_for_vm_status_is_active(vm_id)
        host = self.client.servers.find(id=vm_id)._info['OS-EXT-SRV-ATTR:host']
        return host == target_host

    def wait_for_vm_status_is_active(self, vm_id, retry_delay=5, timeout=60):
        timeout_reached = False
        start_time = time.time()
        while not timeout_reached:
            vm_status = self.client.servers.find(id=vm_id).status
            if vm_status == 'ACTIVE':
                break
            elif vm_status == 'ERROR':
                raise AssertionError("VM is in {} status".format(vm_status))

            time.sleep(retry_delay)
            timeout_reached = (time.time() - start_time) > timeout
        else:
            raise AssertionError("VM did not get status active, "
                                 "VM has '{}' status".format(vm_status))
