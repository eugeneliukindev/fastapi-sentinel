from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.uow import UnitOfWork


class UoWProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_uow(self, session: AsyncSession) -> UnitOfWork:
        # No explicit rollback here: AsyncSession.close() (invoked when the session
        # provider leaves its `async with`) rolls back the transaction whenever it is
        # still active. It keys off uncommitted changes, not the exception — a request
        # that errors before commit() simply never commits, so close() discards it.
        return UnitOfWork(session)
