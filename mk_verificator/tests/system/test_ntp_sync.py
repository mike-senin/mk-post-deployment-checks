import pytest
import json
from mk_verificator import utils


@pytest.mark.parametrize(
    ("group"),
    utils.get_groups(utils.get_configuration(__file__))
)
def test_ntp_sync(group, local_salt_client):

    data = {}
    node_times_list = []
    hour = 0
    minute = 0
    second = 0
    hour_gauge = 0
    minute_gauge = 0
    second_gauge = 5
    divisor = 0

    fail = {}

    nodes_info = local_salt_client.cmd(group, 'cmd.run', ['date +"%H %M %S"'])

    for node, time in nodes_info.iteritems():
        node_times = time.split(' ')
        data[node] = node_times
        node_times_list.append(node_times)

    for time_list in node_times_list:
        hour += int(time_list[0])
        minute += int(time_list[1])
        second += int(time_list[2])
        divisor += 1
    hour = hour / divisor
    minute = minute / divisor
    second = second / divisor

    for node in data:
        ntime = data.get(node)

        if (int(ntime[0]) - hour) != hour_gauge:
            fail[node] = "{}h {}m {}s".format(ntime[0], ntime[1], ntime[2])
        elif (int(ntime[1]) - minute) != minute_gauge:
            fail[node] = "{}h {}m {}s".format(ntime[0], ntime[1], ntime[2])
        elif (int(ntime[2]) - second) > second_gauge:
            # TODO: add correct verification for seconds difference
            fail[node] = "{}h {}m {}s".format(ntime[0], ntime[1], ntime[2])

    assert not fail, 'AVG time: {}h {}m {}s\nNodes with ' \
                     'time mismatch: {}'.format(hour, minute, second, fail)
