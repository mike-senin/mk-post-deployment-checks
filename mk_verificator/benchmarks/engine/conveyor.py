import multiprocessing
import uuid

import pytest
from mk_verificator.benchmarks import plugin


class Conveyor(object):

    def __init__(self, scenarios):
        self.scenarios = scenarios
        manager = multiprocessing.Manager()
        self.shared_memory = manager.dict()

    def start(self):
        for test in self.scenarios:
            step_uuid = str(uuid.uuid4())
            if isinstance(test, list):
                self.multi_process_run(step_uuid, test, self.shared_memory)
            else:
                self.single_process_run(step_uuid, test, self.shared_memory)

    def _runner(self, test_name, shared_memory, step_uuid):
        pytest.main(['-qq'],
                    plugins=[plugin.BenchmarkPlugin(test_name,
                                                    shared_memory,
                                                    step_uuid)])

    def multi_process_run(self, step_uuid, sub_scenarios, shared_memory):
        processes = {}
        for test_num, test_name in enumerate(sub_scenarios):
            p = multiprocessing.Process(
                target=self._runner,
                args=(test_name,
                      shared_memory,
                      step_uuid + str(test_num)),
            )
            processes[test_num] = (p, p.pid, p.is_alive())

        for process, _, _ in processes.values():
            process.start()

        for process, _, _ in processes.values():
            process.join()

    def single_process_run(self, step_uuid, test_name, shared_memory):
        self._runner(test_name, shared_memory, step_uuid)
