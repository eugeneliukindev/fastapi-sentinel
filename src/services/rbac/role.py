from src.core.uow import UnitOfWork
from src.dto.rbac.role import RoleInsert
from src.exceptions.rbac import InsufficientPermissionsError
from src.models.rbac.role import RoleEnum
from src.schemas.rbac.role import RoleRead


class RoleService:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def list_roles(self) -> list[RoleRead]:
        roles = await self._uow.roles.list()
        return [RoleRead.model_validate(r) for r in roles]

    async def create_role(self, name: RoleEnum) -> RoleRead:
        role = await self._uow.roles.add(RoleInsert(name=name))
        await self._uow.commit()
        return RoleRead.model_validate(role)

    async def delete_role(self, role_id: int) -> RoleRead:
        role = await self._uow.roles.delete(role_id)
        if role is None:
            raise InsufficientPermissionsError
        await self._uow.commit()
        return RoleRead.model_validate(role)

    async def assign_permission(self, role_id: int, permission_id: int) -> RoleRead:
        role = await self._uow.roles.get_by_id(role_id)
        permission = await self._uow.permissions.get_by_id(permission_id)
        if role is None or permission is None:
            raise InsufficientPermissionsError
        role.permissions.add(permission)
        await self._uow.commit()
        return RoleRead.model_validate(role)

    async def revoke_permission(self, role_id: int, permission_id: int) -> RoleRead:
        role = await self._uow.roles.get_by_id(role_id)
        permission = await self._uow.permissions.get_by_id(permission_id)
        if role is None or permission is None:
            raise InsufficientPermissionsError
        role.permissions.discard(permission)
        await self._uow.commit()
        return RoleRead.model_validate(role)
