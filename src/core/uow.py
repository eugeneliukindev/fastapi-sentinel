from functools import cached_property
from types import TracebackType
from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession

from src.repo import PermissionRepository, RoleRepository, TokenBlacklistRepository, UserRepository


class UnitOfWork:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @property
    def session(self) -> AsyncSession:
        return self._session

    @cached_property
    def users(self) -> UserRepository:
        return UserRepository(self._session)

    @cached_property
    def roles(self) -> RoleRepository:
        return RoleRepository(self._session)

    @cached_property
    def permissions(self) -> PermissionRepository:
        return PermissionRepository(self._session)

    @cached_property
    def token_blacklist(self) -> TokenBlacklistRepository:
        return TokenBlacklistRepository(self._session)

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        tb: TracebackType | None,
    ) -> bool:
        if exc_type is not None:
            await self.rollback()
        return False  # do not suppress exceptions; commit is explicit
