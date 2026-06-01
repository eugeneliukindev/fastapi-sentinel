from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from src.api.dependencies.auth import BearerToken, CurrentUser
from src.schemas.auth import AccessTokenResponse, TokenResponse
from src.schemas.user import UserCreate, UserRead
from src.services.auth.service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"], route_class=DishkaRoute)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(data: UserCreate, auth: FromDishka[AuthService]) -> UserRead:
    return await auth.register(data.username, data.password)


@router.post("/login")
async def login(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth: FromDishka[AuthService],
) -> TokenResponse:
    return await auth.login(form.username, form.password)


@router.post("/refresh")
async def refresh(token: BearerToken, auth: FromDishka[AuthService]) -> AccessTokenResponse:
    return await auth.refresh(token)


@router.get("/me")
async def me(user: CurrentUser) -> UserRead:
    return user
