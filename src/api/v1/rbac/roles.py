from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, status

from src.schemas.rbac.role import RoleCreate, RoleRead
from src.services.rbac.role import RoleService

router = APIRouter(prefix="/roles", tags=["roles"], route_class=DishkaRoute)


@router.get("")
async def list_roles(service: FromDishka[RoleService]) -> list[RoleRead]:
    return await service.list_roles()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_role(service: FromDishka[RoleService], data: RoleCreate) -> RoleRead:
    return await service.create_role(data.name)


@router.delete("/{role_id}")
async def delete_role(service: FromDishka[RoleService], role_id: int) -> RoleRead:
    return await service.delete_role(role_id)


@router.post("/{role_id}/permissions/{permission_id}", status_code=status.HTTP_201_CREATED)
async def assign_permission(service: FromDishka[RoleService], role_id: int, permission_id: int) -> RoleRead:
    return await service.assign_permission(role_id, permission_id)


@router.delete("/{role_id}/permissions/{permission_id}", status_code=status.HTTP_204_NO_CONTENT)
async def revoke_permission(service: FromDishka[RoleService], role_id: int, permission_id: int) -> None:
    await service.revoke_permission(role_id, permission_id)
