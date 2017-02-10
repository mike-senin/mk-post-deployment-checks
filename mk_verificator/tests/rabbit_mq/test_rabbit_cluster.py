__author__ = 'pivanets'
import json


def test_checking_rabbitmq_cluster(local_salt_client):
    cs = local_salt_client.cmd(
        'rmq*',
        'cmd.run',
        ['salt-call pillar.data --output json rabbitmq:cluster'])

    # create dictionary {node:required_cluster_size} that will be
    # compared to actual cluster size
    required_cluster_size_dict = {}

    [required_cluster_size_dict.update(
        {node: len(cs.keys())}) for node in cs.keys()]

    # in case if node cluster size differs from the required one, control dictionary
    # is updated with {node:cluster_size_from_the_node}
    control_dict = {}
    for node in cs:
        data = json.loads(cs[node])

        cluster_size_from_the_node = len(data['local']['rabbitmq:cluster']['members'])
        if required_cluster_size_dict[node] != cluster_size_from_the_node:
            control_dict.update({node:cluster_size_from_the_node})

    assert not len(control_dict), \
        '''Inconsistency found within cloud. RabbitMQ cluster
              is probably broken, the cluster size for each node should be:
              {} but the following nodes has other values: {}'''.format(len(cs.keys()),
                                                                        control_dict)
