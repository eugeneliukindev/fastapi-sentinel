from collections.abc import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from config import Settings


class DatabaseProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_engine(self, settings: Settings) -> AsyncIterable[AsyncEngine]:
        engine = create_async_engine(settings.db.url)
        yield engine
        await engine.dispose()  # container.close() in lifespan

    @provide(scope=Scope.APP)
    def get_async_sessionmaker(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(engine, expire_on_commit=False, autoflush=False)

    @provide(scope=Scope.REQUEST)
    async def get_async_session(self, sessionmaker: async_sessionmaker[AsyncSession]) -> AsyncIterable[AsyncSession]:
        # `async with` always calls session.close() on exit, which rolls back the
        # transaction whenever it is still active. It keys off uncommitted changes,
        # not the exception — a request that errors before commit() simply never
        # commits, so close() discards it. No try/except rollback needed (dishka
        # finalizes via asend, not athrow, so except would not fire anyway).
        async with sessionmaker() as session:
            yield session
