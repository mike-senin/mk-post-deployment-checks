def test_checking_nova_compute(local_salt_client):
    service_info = local_salt_client.cmd(
        'cpu*', 
        'cmd.run', 
       ['service nova-compute status'])

    computes_no_availability = []

    for node in service_info:
        if not 'nova-compute start/running,' in service_info[node]:
            computes_no_availability.append(node)

    assert not computes_no_availability, \
        "Nodes where nova-compute isn't started: {}".format(computes_no_availability)
