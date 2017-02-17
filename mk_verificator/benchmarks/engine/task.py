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

        # self.scenario_args = None

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
        results = {}
        for task_phase in ['setup', 'main', 'teardown']:
            # TODO
            phase_results = {'results': '', 'state': '', 'exceptions': None}
            try:
                # TODO (msenin) return result within functions
                # and do not use intermediate variable
                getattr(self.scenario_body, task_phase)()
                self.state = 'finished'
            except Exception as e:
                self.state = 'error'
                phase_results['exceptions'] = str(e)
            finally:
                phase_results['results'] = self.scenario_body.result
                phase_results['state'] = str(self.state)
                results[task_phase] = phase_results

        results_array[self.uuid] = results
