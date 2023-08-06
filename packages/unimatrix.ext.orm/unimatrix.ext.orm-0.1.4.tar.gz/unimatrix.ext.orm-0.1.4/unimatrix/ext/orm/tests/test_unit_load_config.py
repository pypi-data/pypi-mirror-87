# pylint: skip-file
import unittest

from unimatrix.ext.orm.conf import load_config


class DatabaseConfigurationTestCase(unittest.TestCase):

    def test_env_sqlite_memory(self):
        env = {
            'DB_ENGINE': "sqlite",
            'DB_NAME': ":memory:"
        }
        connections = load_config(env)
        self.assertEqual(connections['self'].as_dsn(), "sqlite://")

    def test_env_sqlite_disk_unix_absolute(self):
        env = {
            'DB_ENGINE': "sqlite",
            'DB_NAME': "/tmp/foo.sqlite3"
        }
        connections = load_config(env)
        self.assertEqual(connections['self'].as_dsn(), "sqlite:////tmp/foo.sqlite3")

    def test_env_sqlite_disk_unix_relative(self):
        env = {
            'DB_ENGINE': "sqlite",
            'DB_NAME': "tmp/foo.sqlite3"
        }
        connections = load_config(env)
        self.assertEqual(connections['self'].as_dsn(), "sqlite:///tmp/foo.sqlite3")
