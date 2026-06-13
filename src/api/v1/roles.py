from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends

from src.api.dependencies.auth import require_role
from src.api.responses import AUTH_RESPONSES
from src.enums import RoleEnum
from src.schemas.role import RoleReadSchema
from src.services.role import RoleService

router = APIRouter(
    prefix="/roles",
    tags=["roles"],
    route_class=DishkaRoute,
    dependencies=[Depends(require_role(RoleEnum.ADMIN))],
    responses=AUTH_RESPONSES,
)


@router.get("")
async def get_all_roles(service: FromDishka[RoleService]) -> list[RoleReadSchema]:
    """Get a list of all roles. Requires ADMIN role."""
    return await service.get_all_roles()
