import time
import random
from mk_verificator.benchmarks.engine.scenario import Scenario

class ScenarioTwo(Scenario):

    result = None

    def __init__(self):
        self.name = '2'


    def setup(self):
        print "Setup %s with param %s" % (self.__class__.__name__, self.name)
        raise Exception('I\'m gonna raise exception in the setup')

    def main(self):
        print "Start %s with param %s" % (self.__class__.__name__, self.name)
        print "I'm gonna sleep 20 sec. %s with param %s" % (
            self.__class__.__name__, self.name)
        time.sleep(20)
        self.result = 'bah, babah'


    def teardown(self):
        print "Teardown %s with param %s" % (self.__class__.__name__, self.name)




