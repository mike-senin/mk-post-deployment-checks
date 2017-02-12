from abc import ABCMeta, abstractproperty, abstractmethod
from functools import reduce


class DerivationRegistry(type):
    def __init__(cls, name, bases, cls_dict):
        type.__init__(cls, name, bases, cls_dict)
        cls._subclasses = set()
        for base in bases:
            if isinstance(base, DerivationRegistry):
                base._subclasses.add(cls)

    def getSubclasses(cls):
        return reduce(
                set.union,
                (succ.getSubclasses() for succ in cls._subclasses if
                 isinstance(succ, DerivationRegistry)),
                cls._subclasses
        )


class ScenarioMixin(ABCMeta, DerivationRegistry):
    def __init__(cls, name, bases, attr):
        ABCMeta.__init__(cls, name, bases, attr)
        DerivationRegistry.__init__(cls, name, bases, attr)


class Scenario(object):
    __metaclass__ = ScenarioMixin

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


