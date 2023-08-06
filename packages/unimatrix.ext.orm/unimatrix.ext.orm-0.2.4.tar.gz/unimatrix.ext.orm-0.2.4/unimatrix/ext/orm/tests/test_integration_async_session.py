# pylint: skip-file
import asyncio
import unittest

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import select
from sqlalchemy.ext.declarative import declarative_base

from .. import create_engine
from .. import destroy_engines
from .. import async_session
from ..conf import load_config


class AsyncSessionTestCase(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine(
            use_async=True,
            databases=load_config({
                'DB_ENGINE': 'sqlite',
                'DB_NAME': ":memory:"
            })
        )
        self.session = async_session()

    def tearDown(self):
        destroy_engines()

    def test_async_create_metadata(self):
        async def f():
            async with self.engine.begin() as engine:
                await engine.run_sync(Base.metadata.create_all)

            async with self.session as session:
                session.add(TestModel(id=1))

                q = select(TestModel).filter(TestModel.id==1)
                result = await session.execute(q)
                dao = result.scalars().first()
                self.assertEqual(dao.id, 1)

        asyncio.run(f())


Base = declarative_base()

class TestModel(Base):
    __test__ = False
    __tablename__ = 'testmodel'

    id = Column(Integer, primary_key=True)
