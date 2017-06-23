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
        ['cat /etc/apt/sources.list.d/*;'
         'cat /etc/apt/sources.list|grep deb|grep -v "#"'],
        expr_form='pcre')
    actual_repo_list = [item.replace('/ ', ' ')
                        for item in raw_actual_info.values()[0].split('\n')]
    expected_salt_data = [repo['source'].replace('/ ', ' ')
                          for repo in info_salt.values()[0]
                          ['linux:system:repo'].values()]

    diff = {}
    my_set = set()

    my_set.update(actual_repo_list)
    my_set.update(expected_salt_data)
    import json
    for repo in my_set:
        rows = []
        if repo not in actual_repo_list:
            rows.append("{}: {}".format("pillars", "+"))
            rows.append("{}: No repo".format('config'))
            diff[repo] = rows
        elif repo not in expected_salt_data:
            rows.append("{}: {}".format("config", "+"))
            rows.append("{}: No repo".format('pillars'))
            diff[repo] = rows
    assert len(diff) <= 1, \
        "Several problems found for {0} group: {1}".format(
        group, json.dumps(diff, indent=4))
