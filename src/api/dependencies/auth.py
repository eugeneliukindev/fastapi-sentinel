from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from starlette import status

from src.schemas.user import UserReadS
from src.services.auth.service import AuthService
from src.services.user import UserService

# HTTPBearer is used because it accepts a raw JWT in the header (Authorization: Bearer <token>) without OAuth2 flow.
# OAuth2PasswordBearer enforces a form-based login (application/x-www-form-urlencoded) with username/password via tokenUrl.
# We use JSON login instead of OAuth2 form data, so HTTPBearer is simpler and more appropriate.
_http_bearer = HTTPBearer()
BearerTokenDep = Annotated[str, Depends(lambda c=Depends(_http_bearer): c.credentials)]


@inject
async def get_current_user(
    token: BearerTokenDep,
    auth_service: FromDishka[AuthService],
    user_service: FromDishka[UserService],
) -> UserReadS:
    payload = await auth_service.access(token)
    return await user_service.get_user_by_id(payload.sub)


CurrentUserDep = Annotated[UserReadS, Depends(get_current_user)]


def require_role(*roles: str):
    @inject
    async def _check(
        token: BearerTokenDep,
        auth_service: FromDishka[AuthService],
        user_service: FromDishka[UserService],
    ) -> None:
        payload = await auth_service.access(token)
        user = await user_service.get_user_by_id_with_roles(payload.sub)
        user_roles = {r.name for r in user.roles}
        if not all(r in user_roles for r in roles):
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
        user_roles = {r.name for r in user.roles}
        if not any(r in user_roles for r in roles):
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
        user_perms = {p.name for role in user.roles for p in role.permissions}
        if not all(p in user_perms for p in permissions):
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
        user_perms = {p.name for role in user.roles for p in role.permissions}
        if not any(p in user_perms for p in permissions):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return _check
