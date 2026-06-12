from src.core.uow import UnitOfWork
from src.schemas.rbac.permission import PermissionReadS


class PermissionService:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def get_all_permissions(self) -> list[PermissionReadS]:
        permissions = await self._uow.permissions.get_all()
        return [PermissionReadS.model_validate(p) for p in permissions]
