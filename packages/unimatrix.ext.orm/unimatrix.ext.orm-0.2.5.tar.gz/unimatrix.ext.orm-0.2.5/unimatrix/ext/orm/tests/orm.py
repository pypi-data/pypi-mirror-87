# pylint: skip-file
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Foo(Base):
    __tablename__ = 'foo'

    bar = Column(Integer, primary_key=True)
