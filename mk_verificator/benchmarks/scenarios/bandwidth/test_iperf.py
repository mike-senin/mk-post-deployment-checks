import pytest
# from mk_verificator import utils


def _start_iperf_between_hosts(salt_client, node_i, node_j):
    # TODO
    # ifaces_info = None
    # local_iface, destination_iface, expected_speed = ifaces_info

    local_iface = 'eth1'
    destination_iface = 'eth1'

    local_ip = _get_ip_by_iface(salt_client, node_i, local_iface)
    destination_ip = _get_ip_by_iface(salt_client, node_j, destination_iface)

    direct_raw_results = _start_iperf_client(
        salt_client, node_i, destination_ip)
    direct_results = _parse_iperf_results(direct_raw_results)

    reverse_raw_results = _start_iperf_client(salt_client, node_j, local_ip)
    reverse_results = _parse_iperf_results(reverse_raw_results)

    return "Direct: {}\nReverse: {}".format(direct_results, reverse_results)


def _parse_iperf_results(minion_raw_output):
    iperf_results = minion_raw_output.values()[0]
    try:
        results = iperf_results.split('\n')[-1][7:]
    except Exception:
        results = str(iperf_results)
    return results


def _get_ip_by_iface(salt_client, minion_name, iface):
    ifaces = salt_client.cmd(minion_name, 'network.ip_addrs', [iface])
    return ifaces.values()[0][0]


def _start_iperf_client(salt_client, minion_name, target_ip,
                        thread_count=None):
    iperf_command = 'iperf -c {0}'.format(target_ip)

    # TODO (msenin) add thread param
    if thread_count:
        iperf_command += ' -P {0}'.format(thread_count)

    result = salt_client.cmd(minion_name, 'cmd.run', [iperf_command])
    return result


@pytest.fixture
def setup(request, local_salt_client):
    local_salt_client.run_job('*', 'cmd.run', ['iperf -s'])

    def teardown():
        local_salt_client.cmd_async('*', 'cmd.run', ['killall -9 iperf'])

    request.addfinalizer(teardown)


# @pytest.mark.skip(
#     reason="test is not finalised, ticket will be assigned to someone else"
# )
# @pytest.mark.parametrize(
#     "sender,receiver,network", [('rmq-01*', 'rmq-02*', 'control-plane')]
#     # utils.get_groups(utils.get_configuration(__file__))
# )
# def test_iperf_hw_hosts(setup, request,
#                         global_results, local_salt_client,
#                         sender, receiver, network):
#     # TODO (msenin) check that iperf installed on node
#
#     results = \
#         _start_iperf_between_hosts(local_salt_client, sender, receiver)
#     global_results.update(request.node.name, results)
