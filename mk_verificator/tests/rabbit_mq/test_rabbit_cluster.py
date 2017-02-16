import json
import re
import pytest
from mk_verificator import utils


@pytest.mark.parametrize(
    ("group"),
    utils.get_groups(utils.get_configuration(__file__))
)
def test_checking_rabbitmq_cluster(local_salt_client, group):
    # request pillar data from rmq nodes
    rabbitmq_pillar_data = local_salt_client.cmd(
        group,
        'cmd.run',
        ['salt-call pillar.data --output json rabbitmq:cluster'])

    # creating dictionary {node:cluster_size_for_the_node}
    # with required cluster size for each node
    control_dict = {}
    required_cluster_size_dict = {}
    for node in rabbitmq_pillar_data:
        data = json.loads(rabbitmq_pillar_data[node])
        cluster_size_from_the_node = \
            len(data['local']['rabbitmq:cluster']['members'])
        required_cluster_size_dict.update({node: cluster_size_from_the_node})

    # request actual data from rmq nodes
    rabbit_actual_data = local_salt_client.cmd(
        group,
        'cmd.run',
        ['rabbitmqctl cluster_status'])

    # find actual cluster size for each node
    for node in rabbit_actual_data:
        list_of_nodes = 0
        for line in rabbit_actual_data[node].split('\n'):
            if 'running_nodes' in line:
                list_of_nodes = re.findall(r'\'rabbit@(.+?)\'',
                                           line,
                                           re.IGNORECASE)

        # update control dictionary with values
        # {node:actual_cluster_size_for_node}
        if required_cluster_size_dict[node] != len(list_of_nodes):
            control_dict.update({node:list_of_nodes})

    assert not len(control_dict), \
        '''Inconsistency found within cloud. RabbitMQ cluster
           is probably broken, the cluster size for each node should be:
           {} but the following nodes has other values: {}'''.format(
        len(required_cluster_size_dict.keys()), control_dict)
