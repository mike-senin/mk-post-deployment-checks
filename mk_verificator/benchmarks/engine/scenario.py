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