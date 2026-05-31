from pydantic import BaseModel

from src.enums import TokenType


class TokenPayload(BaseModel):
    sub: str
    iat: int
    exp: int
    jti: str
    type: TokenType
