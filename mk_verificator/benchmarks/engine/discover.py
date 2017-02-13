import os
from mk_verificator.benchmarks.engine.scenario import Scenario


# TODO (msenin) rename
def discover():
    # get all directories from scenarios folder
    for i in ['test_1', 'test_2']:
        path = "mk_verificator.benchmarks.scenarios.%s.scenario" % i
        __import__(path)

    print Scenario.__subclasses__()