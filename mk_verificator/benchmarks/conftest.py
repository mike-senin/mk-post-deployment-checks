import pytest

from mk_verificator.fixtures.base import *


@pytest.fixture(scope='session')
def global_results(request):
    return request.session.global_results
