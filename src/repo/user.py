from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.dto.user import UserInsertDTO, UserUpdateDTO
from src.models import RoleOrm, UserOrm
from src.repo.base import BaseRepository


class UserRepository(BaseRepository[UserOrm, UserInsertDTO, UserUpdateDTO]):
    model = UserOrm

    async def get_by_email(self, email: str) -> UserOrm | None:
        return await self._session.scalar(select(UserOrm).where(UserOrm.email == email))  # type: ignore[no-any-return]

    async def get_by_id_with_roles(self, id_: int) -> UserOrm | None:
        stmt = select(UserOrm).where(UserOrm.id == id_).options(selectinload(UserOrm.roles))
        return await self._session.scalar(stmt)  # type: ignore[no-any-return]

    async def get_by_id_with_roles_and_permissions(self, id_: int) -> UserOrm | None:
        stmt = (
            select(UserOrm)
            .where(UserOrm.id == id_)
            .options(selectinload(UserOrm.roles).selectinload(RoleOrm.permissions))
        )
        return await self._session.scalar(stmt)  # type: ignore[no-any-return]
