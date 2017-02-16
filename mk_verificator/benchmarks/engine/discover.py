import os

from mk_verificator.benchmarks.engine.scenario import Scenario


# TODO (msenin) rename
def discover():
    # get all directories from scenarios folder
    current_file_path = os.path.abspath(os.path.dirname(__file__))
    scenario_folder = os.path.join(current_file_path, '../scenarios/')

    scenario_folders = filter(
        lambda x: os.path.isdir(os.path.join(scenario_folder, x)),
            os.listdir(scenario_folder)
    )

    for scenario_folder_name in scenario_folders:
        scenario_module = \
            "mk_verificator.benchmarks" \
            ".scenarios.%s.scenario" % scenario_folder_name
        try:
            __import__(scenario_module)
        except ImportError:
            # TODO (msenin) Add logging with warning level here
            pass

    return Scenario.__subclasses__()