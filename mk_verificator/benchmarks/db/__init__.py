from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from db import models


engine = create_engine('sqlite:///file.db')
models.Base.metadata.create_all(engine)
session = Session(engine)


class TasksRepository(object):

    @staticmethod
    def create(task_obj):
        # TODO move to method get_public_values
        values = {
            'state': task_obj.state,
            'uuid': task_obj._uuid,
            'results': task_obj.results,
            'name': task_obj._name
        }
        task = models.Task(**values)
        session.add(task)
        session.commit()

    @staticmethod
    def get(uuid):
        return session.query(models.Task).\
            filter(models.Task.uuid == uuid)

    @staticmethod
    def update(uuid, task_obj):
        task = TasksRepository.get(uuid)
        values = {
            'state': task_obj.state,
            'uuid': task_obj._uuid,
            'results': task_obj.results,
            'name': task_obj._name
        }
        task.update(values)
        session.commit()
