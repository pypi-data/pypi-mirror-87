# pylint: skip-file
import unittest

from .. import create_engine
from .. import destroy_engines
from .. import ENGINES
from .. import ASYNC_ENGINES
from ..conf import load_config


class CreateEngineTestCase(unittest.TestCase):

    def test_engine_is_created(self):
        engine = create_engine('self',
            databases=load_config({'DB_ENGINE': 'sqlite', 'DB_NAME': ':memory:'}))
        self.assertEqual(engine.dialect.name, 'sqlite')

    def test_registry_is_updated(self):
        destroy_engines()
        self.assertEqual(len(ENGINES), 0)
        engine = create_engine('self',
            databases=load_config({'DB_ENGINE': 'sqlite', 'DB_NAME': ':memory:'}))
        self.assertEqual(len(ASYNC_ENGINES), 0)
        self.assertEqual(len(ENGINES), 1)

    def test_async_registry_is_updated(self):
        destroy_engines()
        self.assertEqual(len(ASYNC_ENGINES), 0)
        engine = create_engine('self',
            use_async=True,
            databases=load_config({'DB_ENGINE': 'sqlite', 'DB_NAME': ':memory:'}))
        self.assertEqual(len(ASYNC_ENGINES), 1)
        self.assertEqual(len(ENGINES), 0)
