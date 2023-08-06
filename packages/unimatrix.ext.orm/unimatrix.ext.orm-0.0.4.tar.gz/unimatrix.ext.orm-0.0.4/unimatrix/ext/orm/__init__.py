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


def destroy_engines():
    """Destroys all known engines."""
    for name in list(dict.keys(ENGINES)):
        engine = ENGINES.pop(name)
        asyncio.run(engine.dispose())


def create_engine(name='self', *args, **kwargs):
    """Create an :class:`sqlalchemy.engine.Engine` instance used the named
    connection `name`.
    """
    global ENGINES

    engine_factory = create_async_engine
    databases = kwargs.pop('databases', None) or DATABASES
    use_async = kwargs.pop('use_async', False)
    if name not in ENGINES:
        ENGINES[name] = databases[name]\
            .as_engine(engine_factory, *args, **kwargs)
    return ENGINES[name] if use_async else ENGINES[name].sync_engine


def session_factory(name='self', *args, **kwargs):
    """Create a new session factory for the named connection `name`."""
    return sessionmaker(bind=create_engine(name), *args, **kwargs)


def async_session(name='self'):
    """Create a new asyncronous session for the named connection `name`."""
    engine = create_engine(name, use_async=True)
    return AsyncSession(engine)
