from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, status

from src.schemas.rbac.permission import PermissionCreate, PermissionRead
from src.services.rbac.permission import PermissionService

router = APIRouter(prefix="/permissions", tags=["permissions"], route_class=DishkaRoute)


@router.get("")
async def list_permissions(service: FromDishka[PermissionService]) -> list[PermissionRead]:
    return await service.list_permissions()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_permission(service: FromDishka[PermissionService], data: PermissionCreate) -> PermissionRead:
    return await service.create_permission(data.name)


@router.delete("/{permission_id}")
async def delete_permission(service: FromDishka[PermissionService], permission_id: int) -> PermissionRead:
    return await service.delete_permission(permission_id)
