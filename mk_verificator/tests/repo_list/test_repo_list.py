import pytest

from mk_verificator import utils


@pytest.mark.parametrize(
    "group",
    utils.get_groups(utils.get_configuration(__file__))
)
def test_list_of_repo_on_nodes(local_salt_client, group):
    info_salt = local_salt_client.cmd(
        group, 'pillar.data', ['linux:system:repo'], expr_form='pcre')

    raw_actual_info = local_salt_client.cmd(
        group,
        'cmd.run',
        ['cat /etc/apt/sources.list.d/*;cat /etc/apt/sources.list|grep deb'],
        expr_form='pcre')

    actual_repo_list = [item.replace('/ ', ' ')
                        for item in raw_actual_info.values()[0].split('\n')]

    expected_salt_data = [
        repo['source'].replace('/ ', ' ')
        for repo in info_salt.values()[0]['linux:system:repo'].values()
    ]

    actual_repo_list.sort()
    expected_salt_data.sort()

    assert actual_repo_list == expected_salt_data, \
        "There is difference between salt formula and " \
        "local list of repo on node salt formula - {}" \
        "local list - {}".format(expected_salt_data, actual_repo_list)
