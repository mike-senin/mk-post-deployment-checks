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

    # create dictionary {node:cluster_size_taken_from_the_node}
    actual_cluster_size_dict = {}
    for node in cs:
        data = json.loads(cs[node])
        actual_cluster_size_dict[node] =\
            len(data['local']['rabbitmq:cluster']['members'])

    d1 = required_cluster_size_dict
    d2 = actual_cluster_size_dict
    areEqual = sorted(d1.values()) == sorted(d2.values())\
               and sorted(d1.keys()) == sorted(d2.keys())

    assert areEqual, \
        '''Inconsistency found within cloud. RabbitMQ cluster
              is probably broken, the cluster size gathered from nodes is:
              {} but should be {}'''.format(actual_cluster_size_dict,
                                            required_cluster_size_dict)
