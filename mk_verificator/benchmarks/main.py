import argparse
import time
import yaml

from mk_verificator.benchmarks.engine.discover import discover
from mk_verificator.benchmarks.engine.runner import Runner
from mk_verificator.benchmarks.engine.scheme import PipelineScheme

from mk_verificator.benchmarks.engine import scenario_convertor, \
    filter_scenarios, init_tasks




def cli():
    # 1. discover and show tests
    # 2. run tests
    # 3. show results
    # 4. init database
    pass


def parse_args():
    pass


if __name__ == '__main__':

    # 1. init scheme
    input_scenarios_scheme_file = 'scenario.yaml'
    pipeline_scheme = PipelineScheme(input_scenarios_scheme_file)

    # 2. discover scenarios
    discovered_scenarios = discover()
    import pdb; pdb.set_trace()
    filtered_scenarios = filter_scenarios(discovered_scenarios,
                                          pipeline_scheme)

    scenarios_repository = dict(
        (scenario_class.__name__,
         scenario_class) for scenario_class in filtered_scenarios
    )

    # 3. init tasks
    print scenarios_repository

    tasks = init_tasks(scenarios_repository,
                       pipeline_scheme.scenarios_set)

    # 4. put tasks set to the runner
    # TODO (msenin) move this logic to the engine __init__.py
    runner = Runner(tasks)

    # 5. start tasks

    start_time = time.time()

    runner.start()

    print("--- %s seconds ---" % (time.time() - start_time))

    # 7. collect and publish results
    print(runner.results)