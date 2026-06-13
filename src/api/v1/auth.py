from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, status

from src.api.dependencies.auth import BearerTokenDep
from src.api.responses import UNAUTHORIZED
from src.schemas.auth import LoginRequestSchema, LogoutSchema, TokenResponseSchema
from src.services.auth.service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"], route_class=DishkaRoute, responses=UNAUTHORIZED)


@router.post("/login")
async def login(schema: LoginRequestSchema, service: FromDishka[AuthService]) -> TokenResponseSchema:
    """Authenticate and return access and refresh tokens."""
    return await service.login(schema)


@router.post("/refresh")
async def refresh(token: BearerTokenDep, service: FromDishka[AuthService]) -> TokenResponseSchema:
    """Issue a new access token using a valid refresh token."""
    return await service.refresh(token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(token: BearerTokenDep, schema: LogoutSchema, service: FromDishka[AuthService]) -> None:
    """Invalidate the current session and blacklist the refresh token."""
    await service.logout(token, schema.refresh_token)
