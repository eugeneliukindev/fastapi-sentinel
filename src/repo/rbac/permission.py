from sqlalchemy import select

from src.dto.rbac.permission import PermissionInsert, PermissionUpdate
from src.models.rbac.permission import Permission
from src.repo.base import BaseRepository


class PermissionRepository(BaseRepository[Permission, PermissionInsert, PermissionUpdate]):
    model = Permission

    async def get_by_name(self, name: str) -> Permission | None:
        return await self._session.scalar(select(Permission).where(Permission.name == name))
