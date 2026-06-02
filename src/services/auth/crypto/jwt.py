import uuid
from datetime import UTC, datetime, timedelta

import jwt

from src.config import settings
from src.dto import TokenPayload
from src.enums import TokenType


def encode_token(
    payload: TokenPayload,
    key: str = settings.app.jwt.private_key.get_secret_value(),
    algorithm: str = settings.app.jwt.algorithm,
) -> str:
    return jwt.encode(payload=payload.model_dump(), key=key, algorithm=algorithm)


def decode_token(
    token: str,
    expected_type: TokenType,
    key: str = settings.app.jwt.public_key,
    algorithm: str = settings.app.jwt.algorithm,
) -> TokenPayload:
    decoded = jwt.decode(token, key=key, algorithms=[algorithm])
    payload = TokenPayload(**decoded)
    if payload.type is not expected_type:
        raise jwt.InvalidTokenError
    return payload


def create_token(
    token_type: TokenType,
    subject: str,
    ttl: timedelta,
    key: str = settings.app.jwt.private_key.get_secret_value(),
    algorithm: str = settings.app.jwt.algorithm,
) -> str:
    now = datetime.now(UTC)
    payload = TokenPayload(
        sub=subject,
        type=token_type,
        iat=int(now.timestamp()),
        exp=int((now + ttl).timestamp()),
        jti=uuid.uuid4().hex,
    )
    return encode_token(payload, key, algorithm)


def create_access_token(subject: str, ttl: timedelta = settings.app.jwt.access_ttl) -> str:
    return create_token(TokenType.ACCESS, subject, ttl)


def create_refresh_token(subject: str, ttl: timedelta = settings.app.jwt.refresh_ttl) -> str:
    return create_token(TokenType.REFRESH, subject, ttl)
