from src.core.uow import UnitOfWork
from src.schemas.permission import PermissionReadSchema


class PermissionService:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def get_all_permissions(self) -> list[PermissionReadSchema]:
        permissions = await self._uow.permissions.get_all()
        return [PermissionReadSchema.model_validate(p) for p in permissions]
