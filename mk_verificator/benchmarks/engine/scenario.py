from abc import ABCMeta, abstractproperty, abstractmethod


class Scenario(object):
    __metaclass__ = ABCMeta

    @abstractproperty
    def result(self):
        pass

    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def main(self):
        pass

    @abstractmethod
    def teardown(self):
        pass



# class ScenarioTwo(Scenario):
#
#     result = None
#
#     def __init__(self, param):
#         self.name = param
#
#
#     def main(self):
#         print "Start %s with param %s" % (self.__class__.__name__, self.name)
#         print "I'm gonna sleep 20 sec. %s with param %s" % (
#             self.__class__.__name__, self.name)
#         # time.sleep(20)
#         self.result = 'bah, babah'
#
#
# class ScenarioOne(Scenario):
#
#     result = None
#
#     def __init__(self, param):
#         self.name = param
#
#
#     def main(self):
#         print "Start %s with param %s" % (self.__class__.__name__, self.name)
#         print "I'm gonna sleep 20 sec. %s with param %s" % (
#             self.__class__.__name__, self.name)
#         # time.sleep(20)
#         self.result = 'bah, babah'


