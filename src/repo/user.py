from sqlalchemy import delete, select
from sqlalchemy.orm import selectinload

from src.dto.user import UserInsertDTO, UserUpdateDTO
from src.models import RoleOrm, UserOrm
from src.models.association.user_roles import UserRolesOrm
from src.repo.base import BaseRepository


class UserRepository(BaseRepository[UserOrm, UserInsertDTO, UserUpdateDTO]):
    model = UserOrm

    async def get_by_email(self, email: str) -> UserOrm | None:
        return await self._session.scalar(select(UserOrm).where(UserOrm.email == email))

    async def add_role(self, user_id: int, role_id: int) -> None:
        self._session.add(UserRolesOrm(user_id=user_id, role_id=role_id))

    async def remove_role(self, user_id: int, role_id: int) -> None:
        await self._session.execute(
            delete(UserRolesOrm).where(UserRolesOrm.user_id == user_id, UserRolesOrm.role_id == role_id)
        )

    async def get_by_id_with_roles(
        self,
        id_: int,
    ) -> UserOrm | None:
        stmt = select(UserOrm).where(UserOrm.id == id_).options(selectinload(UserOrm.roles))
        return await self._session.scalar(stmt)

    async def get_by_id_with_roles_and_permissions(
        self,
        id_: int,
    ) -> UserOrm | None:
        stmt = (
            select(UserOrm)
            .where(UserOrm.id == id_)
            .options(selectinload(UserOrm.roles).selectinload(RoleOrm.permissions))
        )
        return await self._session.scalar(stmt)
