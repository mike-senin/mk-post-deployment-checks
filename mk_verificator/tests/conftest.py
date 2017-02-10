import fixtures.base

from _pytest._pluggy import HookspecMarker

# for pep8
_ = fixtures.base

hookspec = HookspecMarker("pytest")


@hookspec(firstresult=True)
def pytest_report_teststatus(report):
    # fail within test case
    if report.when == "call":
        if not report.failed:
            return
    # fail within setup fixture
    elif report.when == "setup":
        if not report.outcome == 'failed':
            return
    else:
        return

    # TODO get results from test and add it as attachment
