# pylint: skip-file
import unittest

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from unimatrix.ext.orm.conf import load_config


class EngineConfigurationTestCase(unittest.TestCase):

    def setUp(self):
        self.connections = load_config({
            'DB_ENGINE': 'sqlite',
            'DB_NAME': ":memory:"
        })
        self.connection = self.connections['self']

    def test_create_engine_from_config(self):
        engine = self.connection.as_engine(create_engine)
        self.assertIsInstance(engine, Engine)
