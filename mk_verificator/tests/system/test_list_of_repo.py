import json
import pytest


@pytest.mark.parametrize(
    ("node"),
    # DOTO get_nodes(get_configuration(__file__))
    ['ctl-01*', 'ctl-02*', 'ctl-03*'])
def test_list_of_repo_on_nodes(local_salt_client, node):
    info_salt = local_salt_client.cmd(
        node,
        'pillar.data',
        ['linux:system:repo'])

    info_cat = local_salt_client.cmd(
        node,
        'cmd.run',
        ['cat /etc/apt/sources.list.d/*;cat /etc/apt/sources.list|grep deb'])

    cat = [item.replace('/ ', ' ')
           for item in info_cat.values()[0].split('\n')]

    salt = [repo['source'].replace('/ ', ' ')
            for repo in info_salt.values()[0]['linux:system:repo'].values()]

    cat.sort()
    salt.sort()

    assert cat == salt, \
        '''There is difference between salt formula and local list of repo on node
              salt formula - {}
              local list - {}'''.format(salt, cat)
