from src.core.uow import UnitOfWork
from src.dto.user import UserInsert
from src.enums import TokenType
from src.exceptions.auth import InvalidCredentialsError, UserAlreadyExistsError
from src.models.user import User
from src.schemas.auth import AccessTokenResponse, TokenResponse
from src.schemas.user import UserRead
from src.services.auth.blacklist import TokenBlacklistService
from src.services.auth.crypto.jwt import create_access_token, create_refresh_token, decode_token
from src.services.auth.crypto.password import get_password_hash, verify_password


class AuthService:
    def __init__(self, uow: UnitOfWork, blacklist_service: TokenBlacklistService) -> None:
        self._uow = uow
        self._blacklist_service = blacklist_service

    async def register(self, username: str, password: str) -> UserRead:
        if await self._uow.users.get_by_username(username) is not None:
            raise UserAlreadyExistsError
        user = await self._uow.users.add(UserInsert(username=username, hashed_password=get_password_hash(password)))
        await self._uow.commit()
        return UserRead.model_validate(user)

    async def login(self, username: str, password: str) -> TokenResponse:
        user: User | None = await self._uow.users.get_by_username(username)
        if user is None or not verify_password(password, user.hashed_password):
            raise InvalidCredentialsError
        subject = str(user.id)
        return TokenResponse(
            access_token=create_access_token(subject),
            refresh_token=create_refresh_token(subject),
        )

    async def logout(self, token: str) -> None:
        payload = decode_token(token, TokenType.REFRESH)
        await self._blacklist_service.blacklist_token(payload)
        await self._uow.commit()

    async def access(self, token: str) -> UserRead:
        user: User = await self._authenticate_by_token(token, TokenType.ACCESS)
        return UserRead.model_validate(user)

    async def refresh(self, token: str) -> AccessTokenResponse:
        user = await self._authenticate_by_token(token, TokenType.REFRESH)
        return AccessTokenResponse(access_token=create_access_token(str(user.id)))

    async def _authenticate_by_token(self, token: str, expected_type: TokenType) -> User:
        payload = decode_token(token, expected_type)
        if await self._blacklist_service.is_blacklisted(payload.jti):
            raise InvalidCredentialsError
        user = await self._uow.users.get_by_id(int(payload.sub))
        if user is None:
            raise InvalidCredentialsError
        return user
