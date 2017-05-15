import pytest
import json
from mk_verificator import utils


@pytest.mark.parametrize(
    "group",
    utils.get_groups(utils.get_configuration(__file__))
)
def test_check_nodes_state(local_salt_client, group):
    config = utils.get_configuration(__file__)

    output = local_salt_client.cmd(
        group, 'state.apply', ['test_state'],
        kwarg={'test': 'True'}, expr_form='pcre')
    errors = {}
    for node in output:
        result = []
        for values in output[node].values():
            if not values['result']:
                if 'The following packages' in values['comment']:
                    list_pkg = local_salt_client.cmd(node, 'lowpkg.list_pkgs')
                    version = list_pkg[node][values['name']]
                    result.append("Package mismatch. "
                                  "Current version is {0}. {1}".
                                  format(version, (values['comment'])))
                else:
                    result.append("Failed. Info: {}".format(values['comment']))
        if not result:
            continue
        elif result not in errors.values():
            errors[node] = result
        else:
            errors[node] = "Same errors"
    assert len(errors.keys()) <= config["skip_number"], \
        "Several problems found for {0} group: {1}".format(
        group, json.dumps(errors, indent=4))
