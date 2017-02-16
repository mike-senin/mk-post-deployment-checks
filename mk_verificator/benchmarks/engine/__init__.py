import yaml
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


def scheme_parser(scheme_path):
    # TODO (msenin) add validator
    scenarios_scheme = yaml.load(open(scheme_path, 'r'))
    return scenarios_scheme


def filter_scenarios(discovered_scenarios, scheme):
    scheme_names = []
    for scenario_scheme in scheme:
        # TODO (msenin) add scheme validator
        # and reduce this code to the generator
        scenario_name = scenario_scheme.get('name')
        scheme_names.append(scenario_name)

    scenarios = []
    for scenario in discovered_scenarios:
        # TODO (msenin) move __name__ to the abstract class as property
        if scenario.__name__ in scheme_names:
            scenarios.append(scenario)

    return scenarios
