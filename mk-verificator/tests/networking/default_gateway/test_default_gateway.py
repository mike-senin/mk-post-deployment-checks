import json
import pytest


@pytest.mark.parametrize(
    ("group"), [
        'ceph*',
        'cmp*',
        'ctl*'
        'saml*'
    ])
def test_check_default_gateways(local_salt_client, group):
    skipped_nodes = ['saml-global-01.mosci.jiocloud.com']

    netstat_info = \
        local_salt_client.cmd(group, 'cmd.run', ['ip r | sed -n 1p'])
    import pdb; pdb.set_trace()

    # TODO
    gw = {}
    for node in netstat_info.items():
        pass

    assert len(gw) != 1, json.dumps(gw, indent=4)
