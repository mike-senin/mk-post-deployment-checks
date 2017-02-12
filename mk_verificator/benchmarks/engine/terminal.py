import argparse

import texttable as tt


def draw_results_table(shared_memory):
    tab = tt.Texttable()
    header = ['test_name', 'test_parameters', 'results', 'exceptions']

    tab.set_cols_align(['r', 'l', 'r', 'l'])
    tab.set_cols_width([20, 20, 20, 60])
    tab.header(header)

    results = {}
    for thread_results in shared_memory.values():
        results.update(thread_results)

    for test_name, data in results.items():

        test_params = '\n'.join(
            ["{}:\t{}".format(name, val)
             for name, val in
             data['test_args'].items() or []]
        )

        if data['exceptions']:
            exceptions = \
                "An exception was occurred on #{} line \n" \
                "Within the file {} \n".format(
                    data['exceptions']['line_number'],
                    data['exceptions']['filepath']
                )
            trace = '\n'.join(data['exceptions']['lines'])
            exceptions += "Trace log:\n{}".format(trace)
        else:
            exceptions = ""
        tab.add_row([
            data['original_test_name'],
            test_params,
            data['results'],
            exceptions
        ])

    represented_table = tab.draw()
    # TODO (msenin)
    print represented_table


def cli():
    parser = argparse.ArgumentParser()

    parser.add_argument("--scenario_file", help="")
    parser.add_argument("--test", default="__all__", help="")
    parser.add_argument("--multiprocess", action="store_true", help="")

    args = parser.parse_args()

    return args
