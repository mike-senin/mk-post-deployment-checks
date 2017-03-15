import pytest


@pytest.fixture(scope='module')
def setup(request):
    print 'setup VM once'

    def teardown():
        print 'delete VM once'

    request.addfinalizer(teardown)


@pytest.mark.parametrize(
    'count_1,block_size_1',
    [(1, 1), (1, 2)]
)
@pytest.mark.parametrize(
    'count,block_size',
    [(1, 1), (1, 2)]
)
def test_dd(setup, request, global_results,
            count, block_size, count_1, block_size_1):
    global_results.update(request.node.name, (count, block_size))


def test_sub_2(request, global_results):
    global_results.update(request.node.name, 2)
    raise Exception
