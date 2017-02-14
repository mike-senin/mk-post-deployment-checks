from mk_verificator.benchmarks.engine.task import Task
from mk_verificator.benchmarks.engine.scenario import Scenario


def scenario_convertor(scenarios):
    tasks = []

    for scenario in scenarios:

        if isinstance(scenario, list):
            task = scenario_convertor(scenario)
            tasks.append(task)
        elif isinstance(scenario, Scenario):
            task = Task(scenario)
            tasks.append(task)
        else:
            # TODO (msenin) specify custom exception / logging
            print('Can\'t convert scenario to task')
            # raise Exception('Can\'t convert scenario to task')

    return tasks
