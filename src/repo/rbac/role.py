from sqlalchemy import select

from src.dto.rbac.role import RoleInsert, RoleUpdate
from src.models.rbac.role import Role, RoleEnum
from src.repo.base import BaseRepository


class RoleRepository(BaseRepository[Role, RoleInsert, RoleUpdate]):
    model = Role

    async def get_by_name(self, name: RoleEnum) -> Role | None:
        return await self._session.scalar(select(Role).where(Role.name == name))
