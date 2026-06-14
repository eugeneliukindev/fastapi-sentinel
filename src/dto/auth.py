from typing import Annotated

from pydantic import BaseModel, BeforeValidator, field_serializer

from src.enums import TokenType

_IntFromNumber = Annotated[int, BeforeValidator(int)]


class TokenPayloadDTO(BaseModel):
    sub: int
    iat: _IntFromNumber
    exp: _IntFromNumber
    jti: str
    type: TokenType

    @field_serializer("sub")
    def serialize_sub(self, value: int) -> str:
        # PyJWT validates sub as str per RFC 7519
        return str(value)
