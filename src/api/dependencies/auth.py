from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from starlette import status

from src.schemas.user import UserReadSchema
from src.services.auth.service import AuthService
from src.services.user import UserService

_http_bearer = HTTPBearer()
BearerTokenDep = Annotated[str, Depends(lambda c=Depends(_http_bearer): c.credentials)]


@inject
async def get_current_user(
    token: BearerTokenDep,
    auth_service: FromDishka[AuthService],
    user_service: FromDishka[UserService],
) -> UserReadSchema:
    payload = await auth_service.access(token)
    return await user_service.get_user_by_id(payload.sub)


CurrentUserDep = Annotated[UserReadSchema, Depends(get_current_user)]


def require_role(*roles: str):
    @inject
    async def _check(
        token: BearerTokenDep,
        auth_service: FromDishka[AuthService],
        user_service: FromDishka[UserService],
    ) -> None:
        payload = await auth_service.access(token)
        user = await user_service.get_user_by_id_with_roles(payload.sub)
        if not user.has_role(*roles):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return _check


def require_any_role(*roles: str):
    @inject
    async def _check(
        token: BearerTokenDep,
        auth_service: FromDishka[AuthService],
        user_service: FromDishka[UserService],
    ) -> None:
        payload = await auth_service.access(token)
        user = await user_service.get_user_by_id_with_roles(payload.sub)
        if not user.has_any_role(*roles):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return _check


def require_permission(*permissions: str):
    @inject
    async def _check(
        token: BearerTokenDep,
        auth_service: FromDishka[AuthService],
        user_service: FromDishka[UserService],
    ) -> None:
        payload = await auth_service.access(token)
        user = await user_service.get_user_by_id_with_roles_and_permissions(payload.sub)
        if not user.has_permission(*permissions):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return _check


def require_any_permission(*permissions: str):
    @inject
    async def _check(
        token: BearerTokenDep,
        auth_service: FromDishka[AuthService],
        user_service: FromDishka[UserService],
    ) -> None:
        payload = await auth_service.access(token)
        user = await user_service.get_user_by_id_with_roles_and_permissions(payload.sub)
        if not user.has_any_permission(*permissions):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return _check
