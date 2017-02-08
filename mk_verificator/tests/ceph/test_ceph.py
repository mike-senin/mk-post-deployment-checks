def test_check_ceph_osd(local_salt_client):
    osd_fail_count = \
        local_salt_client.cmd('ceph-001*', 'cmd.run',
                              ['ceph osd tree | grep down | wc -l'])

    assert osd_fail_count.values()[0] == '0', \
        "Some osd are in down state ({} in total).".format(
        osd_fail_count.values()[0])
