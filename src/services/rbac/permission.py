from src.core.uow import UnitOfWork
from src.dto.rbac.permission import PermissionInsert
from src.exceptions.rbac import InsufficientPermissionsError
from src.schemas.rbac.permission import PermissionRead


class PermissionService:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def list_permissions(self) -> list[PermissionRead]:
        permissions = await self._uow.permissions.list()
        return [PermissionRead.model_validate(p) for p in permissions]

    async def create_permission(self, name: str) -> PermissionRead:
        permission = await self._uow.permissions.add(PermissionInsert(name=name))
        await self._uow.commit()
        return PermissionRead.model_validate(permission)

    async def delete_permission(self, permission_id: int) -> PermissionRead:
        permission = await self._uow.permissions.delete(permission_id)
        if permission is None:
            raise InsufficientPermissionsError
        await self._uow.commit()
        return PermissionRead.model_validate(permission)
