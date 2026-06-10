from collections.abc import Callable, Coroutine
from typing import Annotated, Any

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from src.exceptions.rbac import InsufficientPermissionsError
from src.models.rbac.role import RoleEnum
from src.schemas.user import UserRead
from src.services.auth.service import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/login")
BearerToken = Annotated[str, Depends(oauth2_scheme)]


@inject
async def get_user_from_access_token(token: BearerToken, auth: FromDishka[AuthService]) -> UserRead:
    return await auth.access(token)


CurrentUser = Annotated[UserRead, Depends(get_user_from_access_token)]


def require_permission(permission: str) -> Callable[[UserRead], Coroutine[Any, Any, UserRead]]:
    async def _check(user: CurrentUser) -> UserRead:
        if permission not in {p.name for p in user.role.permissions}:
            raise InsufficientPermissionsError
        return user

    return _check


def require_role(role: RoleEnum) -> Callable[[UserRead], Coroutine[Any, Any, UserRead]]:
    async def _check(user: CurrentUser) -> UserRead:
        if user.role.name != role:
            raise InsufficientPermissionsError
        return user

    return _check
