"""Provides functions to configure the database connection(s)."""
import copy
import os

import unimatrix.lib.rdbms


class DatabaseConnection(dict):
    """Represents a database connection configuration."""

    def as_dsn(self):
        """Returns the connection credentials as a data source name."""
        if self['engine'] and self.get('name') == ':memory:':
            return "sqlite://"
        elif self['engine'] == 'sqlite':
            return f"sqlite:///{self['name']}"
        else:
            raise NotImplementedError

    def as_engine(self, create_engine, *args, **kwargs):
        """Return a :class:`sqlalchemy.engine.Engine` instance configured
        with the connection parameters.
        """
        return create_engine(self.as_dsn(), *args, **kwargs)


def load_config(*args, **kwargs):
    """Like :func:`~unimatrix.lib.rdbms.load_config`, but returns a mapping
    of :class:`DatabaseConnection` objects.
    """
    connections = unimatrix.lib.rdbms.load_config(*args, **kwargs)
    for name, opts in dict.items(connections):
        connections[name] = DatabaseConnection(**opts)
    return connections


DATABASES = load_config(env=copy.deepcopy(os.environ))
