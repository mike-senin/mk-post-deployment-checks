from mk_verificator.benchmarks.engine.discover import discover

if __name__ == '__main__':
    discover()

    # print(Scenario.getSubclasses())


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
