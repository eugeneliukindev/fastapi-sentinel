from src.core.uow import UnitOfWork
from src.schemas.rbac.role import RoleReadS


class RoleService:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def get_all_roles(self) -> list[RoleReadS]:
        roles = await self._uow.roles.get_all()
        return [RoleReadS.model_validate(r) for r in roles]
