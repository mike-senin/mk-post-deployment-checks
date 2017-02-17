import time
import random
from mk_verificator.benchmarks.engine.scenario import Scenario


class ScenarioOne(Scenario):

    result = None

    def __init__(self, param):
        self.property_1 = param

    def setup(self):
        print "Setup %s with param %s" % (self.__class__.__name__, self.property_1)

    def main(self):
        time.sleep(random.randint(1, 15))
        print "Start %s with param %s" % (self.__class__.__name__, self.property_1)
        self.result = 'bah, babah'

    def teardown(self):
        print "Teardown %s with param %s" % (self.__class__.__name__,
                                             self.property_1)
        raise Exception('I\'m gonna raise exception in the teardown')

