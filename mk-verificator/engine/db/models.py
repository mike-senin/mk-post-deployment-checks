from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, JSON, create_engine

Base = declarative_base()


class Task(Base):

    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, unique=True)
    results = Column(JSON)
    uuid = Column(String)
    name = Column(String)
    state = Column(String)

    def __init__(self, results, uuid, name, state):
        self.results = results
        self.uuid = uuid
        self.name = name
        self.state = state


    # TODO
    # def __repr__(self):
    #     pass


class Scenario():
    pass


def init_base():
    pass



