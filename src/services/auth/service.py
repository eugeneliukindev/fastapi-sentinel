from src.core.uow import UnitOfWork
from src.enums import TokenType
from src.exceptions.auth import InvalidCredentialsError, UserAlreadyExistsError
from src.models.user import User
from src.schemas.auth import AccessTokenResponse, TokenResponse
from src.schemas.user import UserRead
from src.services.auth.password import get_password_hash, verify_password
from src.services.auth.tokens import create_access_token, create_refresh_token, decode_token


class AuthService:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def register(self, username: str, password: str) -> UserRead:
        if await self._uow.users.get_by_username(username) is not None:
            raise UserAlreadyExistsError
        user = User(username=username, hashed_password=get_password_hash(password))
        await self._uow.users.add(user)
        await self._uow.commit()
        return UserRead.model_validate(user)

    async def login(self, username: str, password: str) -> TokenResponse:
        user = await self._authenticate(username, password)
        subject = str(user.id)
        return TokenResponse(
            access_key=create_access_token(subject),
            refresh_key=create_refresh_token(subject),
        )

    async def refresh(self, refresh_token: str) -> AccessTokenResponse:
        user = await self.authenticate_by_token(refresh_token, TokenType.REFRESH)
        return AccessTokenResponse(access_key=create_access_token(str(user.id)))

    async def authenticate_by_token(self, token: str, token_type: TokenType) -> UserRead:
        payload = decode_token(token, token_type)
        user = await self._uow.users.get_by_id(int(payload.sub))
        if user is None:
            raise InvalidCredentialsError
        return UserRead.model_validate(user)

    async def _authenticate(self, username: str, password: str) -> UserRead:
        user = await self._uow.users.get_by_username(username)
        if user is None or not verify_password(password, user.hashed_password):
            raise InvalidCredentialsError
        return UserRead.model_validate(user)
