from mk_verificator import utils


def test_ceph_haproxy(local_salt_client):
    config = utils.get_configuration(__file__)

    fail = {}

    for monitor in config["ceph_monitors"]:
        monitor_info = local_salt_client.cmd(monitor, 'cmd.run',
                                             ["echo 'show stat' | nc -U "
                                              "/var/run/haproxy/admin.sock | "
                                              "grep ceph_mon_radosgw_cluster"])

        for name, info in monitor_info.iteritems():
            if "OPEN" and "UP" in info:
                continue
            else:
                fail[name] = info

    assert not fail, "Failed monitors: {}".format(fail)
