def test_ntp_sync(local_salt_client):

    data = {}
    node_times_list = []
    h = 0
    m = 0
    s = 0
    h_gauge = 0
    m_gauge = 0
    s_gauge = 5
    divisor = -1

    fail = {}

    nodes_info = local_salt_client.cmd('*', 'cmd.run', ['date +"%H %M %S"'])

    for node, time in nodes_info.iteritems():
        node_times = time.split(' ')
        data[node] = node_times
        node_times_list.append(node_times)

    for time_list in node_times_list:
        h += int(time_list[0])
        m += int(time_list[1])
        s += int(time_list[2])
        divisor += 1
    h = h/divisor
    m = m/divisor
    s = s/divisor

    for node in data:
        ntime = data.get(node)

        if (int(ntime[0]) - h) != h_gauge:
            fail[node] = ntime
        elif (int(ntime[1]) - m) != m_gauge:
            fail[node] = ntime
        elif (int(ntime[2]) - s) > s_gauge:
            # TODO: add correct verification for seconds difference
            fail[node] = ntime

    assert not fail, 'Nodes with time mismatch: {}'.format(fail)
