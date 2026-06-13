from src.core.uow import UnitOfWork
from src.schemas.role import RoleReadSchema


class RoleService:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def get_all_roles(self) -> list[RoleReadSchema]:
        roles = await self._uow.roles.get_all()
        return [RoleReadSchema.model_validate(r) for r in roles]
