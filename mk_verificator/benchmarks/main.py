import yaml

from mk_verificator.benchmarks.engine import terminal
from mk_verificator.benchmarks.engine import conveyor


if __name__ == '__main__':
    args = terminal.cli()

    if args.scenario_file:
        scenarios = yaml.load(open(args.scenario_file, 'r'))
    elif args.test:
        scenarios = [args.test]
    else:
        scenarios = ['__all__']

    conveyor = conveyor.Conveyor(scenarios)
    conveyor.start()

    terminal.draw_results_table(conveyor.shared_memory)
