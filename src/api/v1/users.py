from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends, status

from src.api.dependencies.auth import CurrentUserDep, require_permission, require_role
from src.api.responses import FORBIDDEN, RESOURCE_RESPONSES, UNAUTHORIZED
from src.enums import PermissionEnum, RoleEnum
from src.schemas.user import (
    UserChangePasswordSchema,
    UserCreateSchema,
    UserPartialUpdateSchema,
    UserReadSchema,
    UserResetPasswordSchema,
    UserUpdateSchema,
)
from src.services.user import UserService

router = APIRouter(prefix="/users", tags=["users"], route_class=DishkaRoute, responses=UNAUTHORIZED)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(schema: UserCreateSchema, service: FromDishka[UserService]) -> UserReadSchema:
    """Register a new user account."""
    return await service.create_user(schema)


@router.get("/me")
async def get_current_user(user: CurrentUserDep) -> UserReadSchema:
    """Get the authenticated user's profile."""
    return user


@router.put("/me")
async def replace_current_user(
    user: CurrentUserDep, schema: UserUpdateSchema, service: FromDishka[UserService]
) -> UserReadSchema:
    """Replace the authenticated user's profile with new data."""
    return await service.replace_user(user.id, schema)


@router.patch("/me")
async def update_current_user(
    user: CurrentUserDep, schema: UserPartialUpdateSchema, service: FromDishka[UserService]
) -> UserReadSchema:
    """Partially update the authenticated user's profile."""
    return await service.update_user(user.id, schema)


@router.delete("/me")
async def delete_current_user(user: CurrentUserDep, service: FromDishka[UserService]) -> UserReadSchema:
    """Delete the authenticated user's account."""
    return await service.delete_user(user.id)


@router.post("/me/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_current_user_password(
    user: CurrentUserDep, schema: UserChangePasswordSchema, service: FromDishka[UserService]
) -> None:
    """Change the authenticated user's password."""
    await service.change_password(user.id, schema)


@router.get("", dependencies=[Depends(require_permission(PermissionEnum.USERS_READ))], responses=FORBIDDEN)
async def get_all_users(service: FromDishka[UserService]) -> list[UserReadSchema]:
    """Get a list of all registered users. Requires USERS_READ permission."""
    return await service.get_all_users()


@router.get(
    "/{user_id}",
    dependencies=[Depends(require_permission(PermissionEnum.USERS_READ))],
    responses=RESOURCE_RESPONSES,
)
async def get_user(user_id: int, service: FromDishka[UserService]) -> UserReadSchema:
    """Get a user by ID. Requires USERS_READ permission."""
    return await service.get_user_by_id(user_id)


@router.put(
    "/{user_id}",
    dependencies=[Depends(require_permission(PermissionEnum.USERS_UPDATE))],
    responses=RESOURCE_RESPONSES,
)
async def replace_user(user_id: int, schema: UserUpdateSchema, service: FromDishka[UserService]) -> UserReadSchema:
    """Replace a user's profile by ID. Requires USERS_UPDATE permission."""
    return await service.replace_user(user_id, schema)


@router.patch(
    "/{user_id}",
    dependencies=[Depends(require_permission(PermissionEnum.USERS_UPDATE))],
    responses=RESOURCE_RESPONSES,
)
async def update_user(
    user_id: int, schema: UserPartialUpdateSchema, service: FromDishka[UserService]
) -> UserReadSchema:
    """Partially update a user by ID. Requires USERS_UPDATE permission."""
    return await service.update_user(user_id, schema)


@router.delete(
    "/{user_id}",
    dependencies=[Depends(require_permission(PermissionEnum.USERS_DELETE))],
    responses=RESOURCE_RESPONSES,
)
async def delete_user(user_id: int, service: FromDishka[UserService]) -> UserReadSchema:
    """Delete a user by ID. Requires USERS_DELETE permission."""
    return await service.delete_user(user_id)


@router.post(
    "/{user_id}/password",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_permission(PermissionEnum.USERS_UPDATE))],
    responses=RESOURCE_RESPONSES,
)
async def reset_user_password(user_id: int, schema: UserResetPasswordSchema, service: FromDishka[UserService]) -> None:
    """Reset a user's password by ID. Requires USERS_UPDATE permission."""
    await service.reset_user_password(user_id, schema.new_password)


@router.post(
    "/{user_id}/roles/{role_id}",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role(RoleEnum.ADMIN))],
    responses=RESOURCE_RESPONSES,
)
async def assign_role(user_id: int, role_id: int, service: FromDishka[UserService]) -> UserReadSchema:
    """Assign a role to a user. Requires ADMIN role."""
    return await service.assign_role(user_id, role_id)


@router.delete(
    "/{user_id}/roles/{role_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_role(RoleEnum.ADMIN))],
    responses=RESOURCE_RESPONSES,
)
async def revoke_role(user_id: int, role_id: int, service: FromDishka[UserService]) -> None:
    """Revoke a role from a user. Requires ADMIN role."""
    await service.revoke_role(user_id, role_id)
