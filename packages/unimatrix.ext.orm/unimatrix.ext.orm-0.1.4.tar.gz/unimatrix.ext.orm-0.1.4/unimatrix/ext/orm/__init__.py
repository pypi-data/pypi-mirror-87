"""The :mod:`unimatrix.ext.orm` package provides common ORM functionality
for Unimatrix packages.
"""
import asyncio
import importlib

import sqlalchemy
import sqlalchemy.ext.declarative
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.sql.schema import MetaData
from sqlalchemy.orm import sessionmaker

from .base import Relation
from .conf import DATABASES
from .conf import load_config


ENGINES = {}
ASYNC_ENGINES = {}


def declarative_base(cls=None, class_factory=None, settings=None, apps=None):
    """Like :func:`sqlalchemy.ext.declarative.declarative_base()`, but
    returns a tuple containing the metadata objects for all applications
    that were specified in :attr:`unimatrix.conf.settings.INSTALLED_APPS`.

    Each application must have a submodule/subpackage named ``orm``, which
    exposed a ``metadata`` attribute.

    The list of installed apps may also be provided using the `apps`
    parameter.

    The resulting list of metadata objects is used to create Alembic
    migration scripts.

    Optionally, the `cls` argument may be provided to use a pre-existing
    declarative base class instead. This allows the :func:`declarative_base`
    function to be used with legacy models.

    By default, :func:`sqlalchemy.ext.declarative.declarative_base()` is
    used to create the base class, but another factory may be specified using
    the `class_factory` argument.
    """
    class_factory = class_factory or sqlalchemy.ext.declarative.declarative_base
    Base = cls or (class_factory)()
    target_metadata = []
    apps = apps or getattr(settings, 'INSTALLED_APPS', [])
    if apps:
        for app_qualname in getattr(settings, 'INSTALLED_APPS', []):
            orm_qualname = "%s.orm" % app_qualname
            try:
                orm = importlib.import_module(orm_qualname)
            except ImportError as e:
                # Fail silently - assume that the installed application does
                # not declare an ORM. We do want to catch other ImportError
                # exceptions tho. This is quicky flaky but it works for now.
                if e.args[0] != ("No module named '%s'" %  orm_qualname):
                    raise
                continue
            if isinstance(orm.metadata, MetaData):
                target_metadata.append(orm.metadata)
            elif isinstance(orm.metadata, (list, tuple)):
                target_metadata.extend(orm.metadata)
            else:
                raise TypeError(
                    "%s.metadata is of invalid type." % orm_qualname)

    target_metadata.append(Base.metadata)
    return Base, target_metadata


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
