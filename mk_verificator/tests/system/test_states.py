import pytest
import json
from mk_verificator import utils


@pytest.mark.parametrize(
    ("group"),
    utils.get_groups(utils.get_configuration(__file__))
)

def test_check_nodes_state(local_salt_client, group):
    output = local_salt_client.cmd(group, 'state.apply', ['alex_test'],  kwarg={'test': 'True'})
    errors = {}
    for node in output:
        result = []
        for values in output[node].values():
            if not values['result']:
                if 'The following packages' in values['comment']:
                    version = local_salt_client.cmd(node, 'lowpkg.list_pkgs')[node][values['name']]
                    result.append("Package mismatch. Current version is {0}. {1}".format(version,(values['comment'])))
                else:
                    result.append("Failed. Info: {}".format(values['comment']))
        if result == []:
            continue
        elif result not in errors.values():
            errors[node] = result
        else:
            errors[node] = "Same list"
    assert len(errors.keys()) <= 1, "Several problems found for {0} group: {1}".format(group,json.dumps(errors, indent=4))
