from src.core.uow import UnitOfWork
from src.dto import TokenPayloadDTO
from src.enums import TokenType
from src.exceptions.auth import InvalidCredentialsError
from src.schemas.auth import LoginRequestS, TokenResponseS
from src.services.auth.blacklist import TokenBlacklistService
from src.services.auth.crypto.jwt import create_access_token, create_refresh_token, decode_token
from src.services.auth.crypto.password import verify_password


class AuthService:
    def __init__(self, uow: UnitOfWork, blacklist_service: TokenBlacklistService) -> None:
        self._uow = uow
        self._blacklist_service = blacklist_service

    async def login(self, data: LoginRequestS) -> TokenResponseS:
        if (user := await self._uow.users.get_by_email(data.email)) is None or not await verify_password(
            data.password, user.hashed_password
        ):
            raise InvalidCredentialsError
        return TokenResponseS(
            access_token=create_access_token(user.id),
            refresh_token=create_refresh_token(user.id),
        )

    async def logout(self, token: str) -> None:
        await self._revoke_refresh_token(token)

    async def access(self, token: str) -> TokenPayloadDTO:
        return await self._validate_token(token, TokenType.ACCESS)

    async def refresh(self, token: str) -> TokenResponseS:
        payload = await self._revoke_refresh_token(token)
        return TokenResponseS(
            access_token=create_access_token(payload.sub),
            refresh_token=create_refresh_token(payload.sub),
        )

    async def _revoke_refresh_token(self, token: str) -> TokenPayloadDTO:
        payload = await self._validate_token(token, TokenType.REFRESH)
        await self._blacklist_service.blacklist_token(payload)
        await self._uow.commit()
        return payload

    async def _validate_token(self, token: str, expected_type: TokenType) -> TokenPayloadDTO:
        payload = decode_token(token, expected_type)
        if await self._blacklist_service.is_blacklisted(payload.jti):
            raise InvalidCredentialsError
        return payload
