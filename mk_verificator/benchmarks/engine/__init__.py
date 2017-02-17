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


def filter_scenarios(discovered_scenarios, scheme):
    scheme_names = scheme.scenarios_names

    scenarios = []
    for scenario in discovered_scenarios:
        # TODO (msenin) move __name__ to the abstract class as property
        if scenario.__name__ in scheme_names:
            scenarios.append(scenario)

    return scenarios


def init_tasks(scenario_repository, scenarios):


    tasks = []

    for scenario in scenarios:
        if isinstance(scenario, list):
            multitask = init_tasks(scenario_repository, scenario)
            tasks.append(multitask)
        else:
            try:

                scenario_name = scenario['name']
                scenario_kwargs = scenario['params']
                scenario_class = scenario_repository[scenario_name]
                inited_scenario = scenario_class(**scenario_kwargs)

                task = Task(inited_scenario)
                tasks.append(task)

            except:
                # TODO (msenin) specify custom exception / logging
                print('Can\'t convert scenario to task')
                # raise Exception('Can\'t convert scenario to task')

    return tasks
    #
    #
    # tasks = []
    #
    # for scenario in scenarios:
    #     if isinstance(scenario, list):
    #         sub_scenarios = []
    #
    #         for sub_scenario in scenario:
    #             scenario_name = sub_scenario['name']
    #             scenario_kwargs = sub_scenario['params']
    #             scenario_class = scenario_repository[scenario_name]
    #
    #             inited_scenario = scenario_class(**scenario_kwargs)
    #             sub_scenarios.append(inited_scenario)
    #
    #         tasks.append(sub_scenarios)
    #     else:
    #         scenario_name = scenario['name']
    #         scenario_kwargs = scenario['params']
    #         scenario_class = scenario_repository[scenario_name]
    #
    #         inited_scenario = scenario_class(**scenario_kwargs)
    #
    #         tasks.append(inited_scenario)
    #
    # return tasks