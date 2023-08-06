"""Declares various functions to assist in testing with :mod:`sqlalchemy`."""
import asyncio
import copy
import os
import unittest

import ioc
from ioc.loader import import_symbol
from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from unimatrix.ext.orm import Relation
from unimatrix.ext.orm import async_session
from unimatrix.ext.orm import create_engine
from unimatrix.ext.orm import destroy_engines
from unimatrix.ext.orm.conf import load_config
from unimatrix.ext.orm.conf import DATABASES


class AsyncSessionTestCase(unittest.TestCase):
    ioc_session_factory_key = None
    target_metadata = []

    @property
    def context_managers(self):
        return list(dict.values(self.transactions))\
            + list(dict.values(self.sessions))

    def run_sync(self, f, *args, **kwargs):
        return self.loop.run_until_complete(f(*args, **kwargs))

    def setUp(self):
        try:
            self.loop = asyncio.get_event_loop()
        except RuntimeError:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)

        # If metadata is specified, create it using the default
        # connection.
        if self.target_metadata:
            engine = create_engine(use_async=True)
            for metadata in self.target_metadata:
                tx = engine.begin()
                connection = self.run_sync(tx.__aenter__)
                self.run_sync(connection.run_sync, metadata.create_all)

        # Create session objects for all configured connections.
        self.sessions = {}
        self.transactions = {}
        for name in self.get_connections():
            Session = async_session(name)
            self.sessions[name] = session =\
                self.run_sync(Session.__aenter__)

            # Start a transaction and roll it back in the tearDown()
            # method.
            self.transactions[name] = tx = session.begin_nested()
            self.run_sync(tx.__aenter__)
            self.run_sync(session.execute, select(1))

        if self.ioc_session_factory_key:
            ioc.provide(self.ioc_session_factory_key,
                self.get_session, force=True)

    def tearDown(self):
        for name, tx in dict.items(self.transactions):
            self.run_sync(tx.rollback)
        for ctx in dict.values(self.sessions):
            self.run_sync(ctx.__aexit__, None, None, None)

    def execute_query(self, session, q, name='self'):
        """Execute query `q` and return the awaited result."""
        return self.run_sync(session.execute, q)

    def get_connections(self):
        """Return the list holding all connection names."""
        return list(dict.keys(DATABASES))

    def get_session(self, name='self'):
        """Returns the overridden session factory for `name`."""
        return self.sessions[name]

    async def create_all(self, engine, metadata):
        async with engine.begin() as connection:
            metadata.create_all(connection)


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
