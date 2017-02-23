from mk_verificator.benchmarks.engine import ResultsRepo
from _pytest._pluggy import HookspecMarker

hookspec = HookspecMarker("pytest")


class BenchmarkPlugin(object):

    def __init__(self, test_name, shared_memory, thread_uuid):
        self.global_results = ResultsRepo()
        self.shared_memory = shared_memory
        self.thread_uuid = thread_uuid
        # TODO (msenin): add regexp
        self.test_name = test_name

    def pytest_sessionstart(self, session):
        session.global_results = self.global_results

    def pytest_sessionfinish(self, session, exitstatus):
        self.shared_memory[self.thread_uuid] = self.global_results.all

    def pytest_report_teststatus(self, report):
        if report.failed:
            if report.longrepr:
                test_name = report.location[-1]

                # NOTE (msenin) sometimes instead of object longrepr is unicode
                if not getattr(report.longrepr, 'reprcrash'):
                    filepath = report.longrepr.location[0]
                    message = report.longrepr
                    # TODO (msenin)
                    line_number = None
                    lines = []
                else:
                    filepath = report.longrepr.reprcrash.path
                    message = report.longrepr.reprcrash.message
                    line_number = report.longrepr.reprcrash.lineno
                    lines = report.longrepr.reprtraceback.reprentries[0].lines

                trace_data = {
                    'filepath': filepath,
                    'message': message,
                    'line_number': line_number,
                    'lines': lines
                    # TODO (msenin) add 'when' data
                }

                self.global_results.update(
                    test_name, trace_data, 'exceptions'
                )
            else:
                # TODO (msenin)
                print "there is no logs"

    # TODO (msenin): Try to move logic to the pytest_collection_modifyitems
    @hookspec(firstresult=True)
    def pytest_pyfunc_call(self, pyfuncitem):
        # init initial body for results
        parametrize = pyfuncitem.get_marker('parametrize')
        args_names = []
        if parametrize:
            args = parametrize.args[::2]
            for _args_names in args:
                _args_names = _args_names.split(',')
                args_names += _args_names

        all_funcargs = pyfuncitem.funcargs.items()
        test_params = dict(
            (arg_name, arg_value) for arg_name, arg_value in
            all_funcargs
            if arg_name in args_names
        )

        test_name = pyfuncitem.name

        self.global_results.update(
            test_name, test_params, 'test_args'
        )

    def _init_test_results(self, session, item):
        original_name = item.originalname

        if not original_name:
            original_name = item.name

        test_name = item.name

        test_report_body = {
            test_name: {
                'original_test_name': original_name,
                'test_args': None,
                'results': None,
                'exceptions': None
            }
        }

        session.global_results.init(test_report_body)

    def pytest_collection_modifyitems(self, session, config, items):
        # TODO (msenin): add regexp
        # TODO (msenin): change mark for all tests
        if not self.test_name == '__all__':
            selected_items = []
            deselected_items = []

            for item in items:
                # import pdb; pdb.set_trace()
                item_name = item.originalname or item.name
                if item_name == self.test_name:
                    selected_items.append(item)
                else:
                    deselected_items.append(item)

            config.hook.pytest_deselected(items=deselected_items)
            items[:] = selected_items

            for item in selected_items:
                self._init_test_results(session, item)
