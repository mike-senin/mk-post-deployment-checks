from mk_verificator.benchmarks.engine.scenario import Scenario


if __name__ == '__main__':
    # TODO (msenin) add discover class and detector of scenario directories
    scenarios = []
    for i in ['test_1', 'test_2']:
        path = "mk_verificator.benchmarks.scenarios.%s.scenario" % i
        scenarios.append(__import__(path))


    print Scenario.__subclasses__()
    print(Scenario.getSubclasses())


    #
    # tasks = [
    #     Task(ScenarioTwo(param=0)),
    #     [
    #         Task(ScenarioOne(param=1)),
    #         Task(ScenarioOne(param=2)),
    #         Task(ScenarioOne(param=3))
    #     ],
    #     Task(ScenarioTwo(param=5))
    # ]
    # tasks = []

    # for scenario in scenarios:
    #     if isinstance(scenario, list):
    #         for _scenario in scenarios:
    #             pass


    # runner = Runner(tasks)
    # runner.start()
