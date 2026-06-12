from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends, status

from src.api.dependencies.auth import CurrentUserDep, require_permission, require_role
from src.enums import PermissionEnum, RoleEnum
from src.schemas.user import UserCreateS, UserReadS, UserUpdateS
from src.services.user import UserService

router = APIRouter(prefix="/users", tags=["users"], route_class=DishkaRoute)


@router.get("/me")
async def me(user: CurrentUserDep) -> UserReadS:
    return user


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(data: UserCreateS, service: FromDishka[UserService]) -> UserReadS:
    return await service.create_user(data)


@router.get("", dependencies=[Depends(require_role(RoleEnum.ADMIN))])
async def get_all_users(service: FromDishka[UserService]) -> list[UserReadS]:
    return await service.get_all_users()


@router.get("/{user_id}", dependencies=[Depends(require_permission(PermissionEnum.USERS_READ))])
async def get_user(user_id: int, service: FromDishka[UserService]) -> UserReadS:
    return await service.get_user_by_id(user_id)


@router.put("/{user_id}", dependencies=[Depends(require_permission(PermissionEnum.USERS_UPDATE))])
async def replace_user(user_id: int, data: UserCreateS, service: FromDishka[UserService]) -> UserReadS:
    return await service.update_user(user_id, UserUpdateS(**data.model_dump()))


@router.patch("/{user_id}", dependencies=[Depends(require_permission(PermissionEnum.USERS_UPDATE))])
async def update_user(user_id: int, data: UserUpdateS, service: FromDishka[UserService]) -> UserReadS:
    return await service.update_user(user_id, data)


@router.delete("/{user_id}", dependencies=[Depends(require_permission(PermissionEnum.USERS_DELETE))])
async def delete_user(user_id: int, service: FromDishka[UserService]) -> UserReadS:
    return await service.delete_user(user_id)


@router.post(
    "/{user_id}/roles/{role_id}",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role(RoleEnum.ADMIN))],
)
async def assign_role(user_id: int, role_id: int, service: FromDishka[UserService]) -> UserReadS:
    return await service.assign_role(user_id, role_id)


@router.delete(
    "/{user_id}/roles/{role_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_role(RoleEnum.ADMIN))],
)
async def revoke_role(user_id: int, role_id: int, service: FromDishka[UserService]) -> None:
    await service.revoke_role(user_id, role_id)
