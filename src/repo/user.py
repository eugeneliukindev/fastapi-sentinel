from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.dto.user import UserInsert, UserUpdate
from src.models.rbac.role import Role
from src.models.user import User
from src.repo.base import BaseRepository


class UserRepository(BaseRepository[User, UserInsert, UserUpdate]):
    model = User

    async def get_by_username(self, username: str) -> User | None:
        return await self._session.scalar(select(User).where(User.username == username))

    async def get_by_id_with_role_and_permissions(self, user_id: int) -> User | None:
        return await self._session.scalar(
            select(User).where(User.id == user_id).options(selectinload(User.role).selectinload(Role.permissions))
        )
