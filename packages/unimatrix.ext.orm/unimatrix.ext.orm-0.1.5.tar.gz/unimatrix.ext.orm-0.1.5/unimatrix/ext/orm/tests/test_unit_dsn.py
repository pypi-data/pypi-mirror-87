# pylint: skip-file
import unittest

from ..conf import DatabaseConnection


class DatasourceConstructionTestCase(unittest.TestCase):
    
    def test_postgresql_minimal_sync(self):
        conn = DatabaseConnection({
            'engine': "postgresql"
        })
        self.assertEqual(conn.as_dsn(),
            "postgresql+psycopg2://localhost:5432")
    
    def test_postgresql_minimal_host_sync(self):
        conn = DatabaseConnection({
            'engine': "postgresql",
            'host': "rdbms"
        })
        self.assertEqual(conn.as_dsn(),
            "postgresql+psycopg2://rdbms:5432")
    
    def test_postgresql_minimal_port_sync(self):
        conn = DatabaseConnection({
            'engine': "postgresql",
            'port': "1000"
        })
        self.assertEqual(conn.as_dsn(),
            "postgresql+psycopg2://localhost:1000")
    
    def test_postgresql_minimal_name_sync(self):
        conn = DatabaseConnection({
            'engine': "postgresql",
            'name': "rdbms"
        })
        self.assertEqual(conn.as_dsn(),
            "postgresql+psycopg2://localhost:5432/rdbms")
    
    def test_postgresql_username_sync(self):
        conn = DatabaseConnection({
            'engine': "postgresql",
            'username': "rdbms"
        })
        self.assertEqual(conn.as_dsn(),
            "postgresql+psycopg2://rdbms@localhost:5432")
    
    def test_postgresql_username_password_sync(self):
        conn = DatabaseConnection({
            'engine': "postgresql",
            'username': "rdbms",
            'password': "rdbms"
        })
        self.assertEqual(conn.as_dsn(),
            "postgresql+psycopg2://rdbms:rdbms@localhost:5432")
    
    def test_postgresql_full_sync(self):
        conn = DatabaseConnection({
            'engine': "postgresql",
            'host': "rdbms",
            'port': "1111",
            'name': "rdbms",
            'username': "rdbms",
            'password': "rdbms"
        })
        self.assertEqual(conn.as_dsn(),
            "postgresql+psycopg2://rdbms:rdbms@rdbms:1111/rdbms")
