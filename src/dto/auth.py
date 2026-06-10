from pydantic import BaseModel, field_serializer

from src.enums import TokenType


class TokenPayload(BaseModel):
    sub: int
    iat: int
    exp: int
    jti: str
    type: TokenType

    @field_serializer("sub")
    def serialize_sub(self, value: int) -> str:
        return str(value)
