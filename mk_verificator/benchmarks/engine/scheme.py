import yaml


class PipelineScheme(object):

    def __init__(self, scheme_path):
        # TODO (msenin)
        self._scheme = yaml.load(
            open(scheme_path, 'r')
        )

    @property
    def scenarios_names(self):

        scenario_names = set()

        for scenario in self.scenarios_set:
            if isinstance(scenario, list):
                for sub_scenario in scenario:
                    scenario_name = sub_scenario['name']
                    scenario_names.add(scenario_name)
            else:
                scenario_name = scenario['name']
                scenario_names.add(scenario_name)

        return scenario_names

    @property
    def scenarios_set(self):
        return self._scheme

    def validate(self):
        pass