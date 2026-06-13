from pydantic import BaseModel, field_serializer

from src.enums import TokenType


class TokenPayloadDTO(BaseModel):
    sub: int
    iat: int
    exp: int
    jti: str
    type: TokenType

    @field_serializer("sub")
    def serialize_sub(self, value: int) -> str:
        # PyJWT validates sub as str per RFC 7519
        return str(value)
