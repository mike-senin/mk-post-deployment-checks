import multiprocessing as mp


class Runner(object):

    def __init__(self, tasks):
        self._tasks = tasks
        manager = mp.Manager()
        self.results = manager.dict()

    @property
    def tasks(self):
        return self._tasks

    @tasks.setter
    def tasks(self, tasks):
        self._tasks = tasks

    def _exec_tasks(self, tasks):
        processes = {}

        for task in tasks:
            p = mp.Process(
                    target=task.start,
                    args=(self.results,),
                    name=task.uuid
            )
            processes[task.uuid] = (p, p.pid, p.is_alive())

        # TODO (msenin) delete print
        print 'start tasks %s' % str(tasks)

        for process, _, _ in processes.values():
            process.start()

        for process, _, _ in  processes.values():
            process.join()

        # TODO (msenin) delete print
        print 'tasks were finished %s' % str(tasks)
        # TODO (msenin) delete print
        print self.results

    def start(self):
        for task in self.tasks:
            if not isinstance(task, list):
                task = [task]

            self._exec_tasks(task)