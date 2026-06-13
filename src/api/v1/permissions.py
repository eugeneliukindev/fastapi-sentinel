from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends

from src.api.dependencies.auth import require_role
from src.api.responses import AUTH_RESPONSES
from src.enums import RoleEnum
from src.schemas.permission import PermissionReadSchema
from src.services.permission import PermissionService

router = APIRouter(
    prefix="/permissions",
    tags=["permissions"],
    route_class=DishkaRoute,
    dependencies=[Depends(require_role(RoleEnum.ADMIN))],
    responses=AUTH_RESPONSES,
)


@router.get("")
async def get_all_permissions(service: FromDishka[PermissionService]) -> list[PermissionReadSchema]:
    """Get a list of all permissions. Requires ADMIN role."""
    return await service.get_all_permissions()
