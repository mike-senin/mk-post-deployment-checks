import pytest
from mk_verificator import utils


@pytest.mark.parametrize(
    "group",
    utils.get_groups(utils.get_configuration(__file__))
)
def test_ntp_sync(group, local_salt_client):
    fail = {}

    saltmaster_time = int(local_salt_client.cmd('cfg-01*',
                                                'cmd.run',
                                                ['date +%s']).values()[0])

    nodes_time = local_salt_client.cmd(group, 'cmd.run', ['date +%s'])

    for node, time in nodes_time.iteritems():
        if (int(time) - saltmaster_time) > 30 or \
                        (int(time) - saltmaster_time) < -30:
            fail[node] = time

    assert not fail, 'SaltMaster time: {}\nNodes with ' \
                     'time mismatch:\n {}'.format(saltmaster_time, fail)
