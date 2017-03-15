class ResultsRepo(object):

    def __init__(self):
        self._results = {}

    @property
    def all(self):
        return self._results

    def update(self, test_name, value, key='results'):
        self._results[test_name].update({key: value})

    def init(self, data):
        self._results.update(data)
