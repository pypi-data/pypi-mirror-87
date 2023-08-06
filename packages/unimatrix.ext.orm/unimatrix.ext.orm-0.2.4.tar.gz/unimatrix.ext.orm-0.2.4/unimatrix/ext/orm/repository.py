"""Declares :class:`RelationalDatabaseRepository`."""
import ioc


class RelationalDatabaseRepository:
    """A repository implementation for use with :mod:`sqlalchemy`."""

    async def __aenter__(self):
        # Determine if there is a transaction running. If a transaction is
        # running, start a savepoint, else begin a new one.
        begin = self.session.begin
        if self.session.sync_session.in_transaction():
            begin = self.session.begin_nested
        self.tx = begin()
        await self.tx.__aenter__()
        return self

    async def __aexit__(self, cls, exc, tb):
        await self.tx.__aexit__(cls, exc, tb)

