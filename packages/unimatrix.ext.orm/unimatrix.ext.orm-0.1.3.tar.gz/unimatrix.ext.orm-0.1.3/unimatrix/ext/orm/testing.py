"""Declares various functions to assist in testing with :mod:`sqlalchemy`."""
import copy
import os
import unittest

from ioc.loader import import_symbol
from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker

from unimatrix.ext.orm import Relation
from unimatrix.ext.orm.conf import load_config


class TestCase(unittest.TestCase):
    """A :class:`unittest.TestCase` implementation that ensures a clean
    database state between tests.
    """
    default_bases = [Relation]

    #: Additional base classes for SQLAlchemy models.
    bases = None

    @classmethod
    def setUpClass(cls):
        cls.manager = TestDatabaseManager(
            self.default_bases + list(self.bases or []))
        cls.manager.on_setup_class({
            'DB_ENGINE': 'sqlite',
            'DB_NAME': ":memory:"
        })

    def setUp(self):
        """Ensures that all connections, transactions and sessions are
        started.
        """
        self.manager.on_setup(self)

    def tearDown(self):
        """Rolls back all transactions and closes the connections."""
        self.manager.on_teardown()


class TestDatabaseManager:
    """Manages the state of the database(s) during automated tests."""

    def __init__(self, bases):
        self.bases = bases
        self.databases = {}
        self.engines = {}
        self.connections = {}
        self.transactions = {}
        self.sessions = {}
        self.session = None

    def get_session(self, name='self'):
        """Return a session for the named connection."""
        return sessionmaker(bind=self.engines[name])()

    def on_setup_class(self, databases=None):
        """Prepare the database connections to commence testing."""
        # Get the database from the environment and secrets directory, and
        # configure a default connection if one is not specified.
        self.databases = load_config(env=copy.deepcopy(os.environ))
        if not self.databases:
            self.databases = load_config(env={
                'DB_ENGINE': "sqlite",
                'DB_NAME': ":memory:"
            })

        # Loop over the discovered database connections to create the engine
        # objects.
        for name, opts in dict.items(self.databases):
            self.engines[name] = engine = opts.as_engine(create_engine, echo=True)
            if name == 'self':
                for Base in self.bases:
                    Base.metadata.create_all(engine)

    def on_setup(self, testcase):
        """Ensures that all sessions for the configured databases have started
        a transaction.
        """

        # TODO: Use the default engine to create the tables. Multi-database
        # support is not fully implemented like Django, but this is good
        # enough for now.
        for name in dict.keys(self.databases):
            engine = self.engines[name]
            self.connections[name] = connection = engine.connect()
            self.transactions[name] = tx = connection.begin()
            self.sessions[name] = session = sessionmaker(bind=connection)()
            if name == 'self':
                testcase.session = session
            #session.begin_nested()

            #@event.listens_for(session, "after_transaction_end")
            #def restart_savepoint(session, tx):
            #    if tx.nested and not tx._parent.nested:
            #        session.begin_nested()

    def on_teardown(self):
        """Rollback all transactions and dispose the engines."""
        for session in dict.values(self.sessions):
            session.close()
        for tx in dict.values(self.transactions):
            tx.rollback()
        for connection in dict.values(self.connections):
            connection.close()
