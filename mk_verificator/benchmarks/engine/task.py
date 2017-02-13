import uuid

from enum import Enum


class TaskStates(Enum):

    running = 1
    finished = 2
    error = 3


class TaskPhases(Enum):

    initialising = 1
    setup = 2
    main = 3
    teardown = 4


class Task(object):

    def __init__(self, scenario):
        self._id = None
        self._state = TaskStates.running
        self._phase = TaskPhases.initialising
        self._uuid = str(uuid.uuid4())
        self._name = scenario.__class__.__name__
        # TODO (msenin) add update DB
        self.scenario_body = scenario

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self._state = TaskStates[state]

    @property
    def uuid(self):
        return "{uuid}".format( uuid=self._uuid)

    # TODO
    def start(self, results_array):
        for task_phase in ['setup', 'main', 'teardown']:
            results = 'None'
            try:
                getattr(self.scenario_body, task_phase)()
                results = self.scenario_body.result
            except:
                self.state = 'error'
                results = self.scenario_body.result
            finally:
                results_array[self.uuid] = results
                self.state = 'finished'