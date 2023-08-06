# pylint: skip-file
import asyncio
import unittest

from .. import create_engine
from .. import destroy_engines
from .. import async_session
from .. import session_factory
from ..conf import load_config


class SessionTestCase(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine(
            databases=load_config({
                'DB_ENGINE': 'sqlite',
                'DB_NAME': ":memory:"
            })
        )

    def tearDown(self):
        destroy_engines()

    def test_create_session_with_no_arguments(self):
        Session = session_factory()
        self.assertEqual(Session().bind.dialect.name, 'sqlite')

    def test_create_session_with_no_arguments(self):
        async def f():
            async with async_session() as session:
                pass

        asyncio.run(f())
