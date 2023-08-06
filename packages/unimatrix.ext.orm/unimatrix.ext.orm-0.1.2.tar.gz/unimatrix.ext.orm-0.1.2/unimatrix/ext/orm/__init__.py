"""The :mod:`unimatrix.ext.orm` package provides common ORM functionality
for Unimatrix packages.
"""
import asyncio

import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from .base import Relation
from .conf import DATABASES
from .conf import load_config


ENGINES = {}
ASYNC_ENGINES = {}


def destroy_engines():
    """Destroys all known engines."""
    for name in list(dict.keys(ENGINES)):
        engine = ENGINES.pop(name)
        engine.dispose()

    for name in list(dict.keys(ASYNC_ENGINES)):
        engine = ASYNC_ENGINES.pop(name)
        asyncio.run(engine.dispose())


def create_engine(name='self', *args, **kwargs):
    """Create an :class:`sqlalchemy.engine.Engine` instance used the named
    connection `name`.
    """
    global ENGINES
    global ASYNC_ENGINES

    databases = kwargs.pop('databases', None) or DATABASES
    use_async = kwargs.get('use_async', False)

    engine_factory = create_async_engine
    if not use_async:
        engine_factory = sqlalchemy.create_engine
    engines = ENGINES if not use_async else ASYNC_ENGINES
    if name not in engines:
        engines[name] = databases[name]\
            .as_engine(engine_factory, *args, **kwargs)
    return engines[name]


def get_dsn(name='self', use_async=False):
    """Return the Data Source Name (DSN) for the named connection."""
    global DATABASES
    return DATABASES[name].as_dsn(use_async=use_async)


def session_factory(name='self', *args, **kwargs):
    """Create a new session factory for the named connection `name`."""
    return sessionmaker(bind=create_engine(name), *args, **kwargs)


def async_session(name='self'):
    """Create a new asyncronous session for the named connection `name`."""
    engine = create_engine(name, use_async=True)
    return AsyncSession(engine)
