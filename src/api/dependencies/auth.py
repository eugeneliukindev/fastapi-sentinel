from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from src.enums import TokenType
from src.schemas.user import UserRead
from src.services.auth.service import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/login")
BearerToken = Annotated[str, Depends(oauth2_scheme)]


@inject
async def get_user_from_access_token(token: BearerToken, auth: FromDishka[AuthService]) -> UserRead:
    return await auth.authenticate_by_token(token, TokenType.ACCESS)


CurrentUser = Annotated[UserRead, Depends(get_user_from_access_token)]
