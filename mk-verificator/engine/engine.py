import abc
import logging
import six

from time import sleep
from enum import Enum
import uuid

from sqlalchemy import create_engine
from utils import createDaemon
from db import models



class TaskStates(Enum):

    initialising = 1
    running = 2
    finished = 3
    error = 4


@six.add_metaclass(abc.ABCMeta)
class Task(object):

    def __init__(self, name='demo'):
        # TODO
        self._id = None
        self._state = TaskStates.initialising
        self._uuid = str(uuid.uuid4())
        self._results = {}
        # TODO get from args
        self._name = name
        # TODO
        task = models.Task(results=self._results, uuid=self._uuid,
                           state=self._state, name=self._name)


    def update_db(self):
        self.db_session = None
        pass
        # models.Task(self._id, )

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = TaskStates(value)
    
    @property
    def results(self):
        return self._results

    @results.setter
    def results(self, results):
        self._results = results

    @abc.abstractmethod
    def start(self):
        raise NotImplementedError

    def run(self):
        try:
            self.state = TaskStates.running
            self.start()
            self.state = TaskStates.finished
        except Exception as e:
            self.state = TaskStates.error

    def __enter__(self):
        print "Hello"
        bd = create_engine('sqlite:///file.db')
        self.connection = bd.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # TODO
        # close db connection
        # self.connection.
        print "Bue"


class Runner(object):
    def __init__(self, *args, **kwargs):
        self._tasks = []

    def add_task(self, task):
        self._tasks.append(task)

    @property
    def tasks(self):
        return self._tasks

    def start(self):
        for task in self.tasks:
            with task as t:
                t.run()


#-----------------------------------------------------------
class TaskWithoutStartMethod(Task):
    def __init__(self, arg):
        super(TaskWithoutStartMethod, self).__init__()
        pass        

class SucsessfulTask(Task):
    def __init__(self):
        super(SucsessfulTask, self).__init__()
        pass

    def start(self):
        print "I'm running"
        sleep(2)
        print "I'm done"


class FailedTask(Task):
    def __init__(self):
        super(FailedTask, self).__init__()
        pass

    def start(self):
        print "I'm running"
        sleep(2)
        print "I'm done"
        raise Exception


class SaltTask(object):
    def __init__(self, arg):
        super(SaltTask, self).__init__()
        pass

    def start(self):
        pass


if __name__ == '__main__':
    print 1
    #ret_code = createDaemon()

    tasker_state_check = SucsessfulTask()
    print tasker_state_check.state
    tasker_state_check.state = 2
    print tasker_state_check.state
    task_1 = SucsessfulTask()
    task_2 = FailedTask()
    runner = Runner()
    runner.add_task(task_1)
    runner.add_task(task_2)
    runner.start()
    print task_1.state
    print task_2.state

    #open("createDaemon.log", "w").write(str(task_2.state) + "\n")

    #sys.exit(ret_code)

