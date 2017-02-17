import os

from mk_verificator.benchmarks.engine.scenario import Scenario


# TODO (msenin) rename
def discover(_name_filter=None):

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

    discovered_scenarios = Scenario.__subclasses__()

    # TODO (msenin) rename
    if _name_filter:
        discovered_scenarios = [
            i for i in discovered_scenarios if i.name in _name_filter
        ]

    return discovered_scenarios




class ScenarioRepository():

    def __init__(self):
        pass

    def discover(self):
        pass

