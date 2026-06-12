from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from src.schemas.rbac.role import RoleReadS
from src.services.rbac.role import RoleService

router = APIRouter(prefix="/roles", tags=["roles"], route_class=DishkaRoute)


@router.get("")
async def get_all_roles(service: FromDishka[RoleService]) -> list[RoleReadS]:
    return await service.get_all_roles()
