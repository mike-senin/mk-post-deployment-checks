import pytest
from mk_verificator import utils


@pytest.mark.parametrize(
    "group",
    utils.get_groups(utils.get_configuration(__file__)))
def test_pkg_version(local_salt_client, group):

    pkgs_info = local_salt_client.cmd(group, 'lowpkg.list_pkgs')

    groups = {}

    missed_pkgs, version_conflicts = [], []

    for node_name, node_pkgs in pkgs_info.items():
        group_name = node_name.split('-')[0]
        if not groups.has_key(group_name):
            groups[group_name] = [(node_name, node_pkgs)]
        else:
            groups[group_name].append((node_name, node_pkgs))

    for group_name, nodes in groups.items():
        if len(nodes) > 1:
            for node_i in nodes:
                for node_j in nodes:
                    if node_i[0] == node_j[0]:
                        continue

                    node_i_name, node_j_name = node_i[0], node_j[0]
                    node_i_pkgs, node_j_pkgs = node_i[1], node_j[1]

                    for pkg_name in node_i_pkgs:

                        if node_j_pkgs.has_key(pkg_name):
                            i_packet_version = node_i_pkgs[pkg_name]
                            j_packet_version = node_j_pkgs[pkg_name]
                            if i_packet_version != j_packet_version:
                                version_conflicts.append((pkg_name, i_packet_version, j_packet_version))
                        else:
                            i_packet_version = node_i_pkgs[pkg_name]
                            missed_pkgs.append((pkg_name, i_packet_version))

                    if missed_pkgs:
                        assert not missed_pkgs, "Pkgs mismatch for node {} and {}:\n{}"\
                            .format(node_i_name, node_j_name, missed_pkgs)

                    if version_conflicts:
                        assert not version_conflicts, "Version conflicts for node {} and {}:\n{}"\
                            .format(node_i_name, node_j_name, version_conflicts)
        else:
            print "Verification for group %s was skipped due to count of nodes less than 2" % group_name
