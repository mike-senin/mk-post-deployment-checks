import argparse
import time
import yaml

from mk_verificator.benchmarks.engine.discover import discover
from mk_verificator.benchmarks.engine.runner import Runner

from mk_verificator.benchmarks.engine import scenario_convertor, \
    filter_scenarios, scheme_parser




def cli():
    # 1. discover and show tests
    # 2. run tests
    # 3. show results
    # 4. init database
    pass


def parse_args():
    pass


if __name__ == '__main__':
    # 1. discover scenarios
    discovered_scenarios = discover()

    input_scenarios_scheme_file = 'scenario.yaml'

    scenarios_scheme = scheme_parser(input_scenarios_scheme_file)

    scenarios = filter_scenarios(discovered_scenarios,
                                 scenarios_scheme)

    # 3. init scenarios
    # TODO (msenin) ADD skipper for broken tests
    # (when have no possibility to init instance of the class)
    # Also we have to have possibility to pass additional arguments
    # to the tests

    init_scenarios = []

    for scenario_class, scenario_data in zip(scenarios, scenarios_scheme):
        kwargs = scenario_data.get('params')
        init_scenarios.append(scenario_class(**kwargs))

    # 4. convert scenario to the task
    tasks = scenario_convertor(init_scenarios)

    # 5. put tasks set to the runner
    # TODO (msenin) move this logic to the engine __init__.py
    runner = Runner(tasks)

    # 6. start tasks

    runner = Runner(tasks)

    start_time = time.time()

    runner.start()

    print("--- %s seconds ---" % (time.time() - start_time))

    # 7. collect and publish results
    print(runner.results)