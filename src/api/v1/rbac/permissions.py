from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from src.schemas.rbac.permission import PermissionReadS
from src.services.rbac.permission import PermissionService

router = APIRouter(prefix="/permissions", tags=["permissions"], route_class=DishkaRoute)


@router.get("")
async def get_all_permissions(service: FromDishka[PermissionService]) -> list[PermissionReadS]:
    return await service.get_all_permissions()
