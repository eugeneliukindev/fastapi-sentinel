from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, status

from src.api.dependencies.auth import BearerTokenDep
from src.schemas.auth import LoginRequestS, TokenResponseS
from src.services.auth.service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"], route_class=DishkaRoute)


@router.post("/login")
async def login(data: LoginRequestS, service: FromDishka[AuthService]) -> TokenResponseS:
    return await service.login(data)


@router.post("/refresh")
async def refresh(token: BearerTokenDep, service: FromDishka[AuthService]) -> TokenResponseS:
    return await service.refresh(token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(token: BearerTokenDep, service: FromDishka[AuthService]) -> None:
    await service.logout(token)
