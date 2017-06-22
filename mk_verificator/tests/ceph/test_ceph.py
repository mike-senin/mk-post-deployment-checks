from mk_verificator import utils


def test_check_ceph_osd(local_salt_client):
    config = utils.get_configuration(__file__)
    osd_fail = \
        local_salt_client.cmd(config["ceph_osd_probe_node"][0], 'cmd.run',
                              ['ceph osd tree | grep down'])
    assert not osd_fail.values()[0], \
        "Some osds are in down state or ceph is not found".format(
        osd_fail.values()[0])
