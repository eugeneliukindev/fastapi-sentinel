from typing import Any, TypeAlias

from fastapi import status

_ResponseType: TypeAlias = dict[int | str, dict[str, Any]]

UNAUTHORIZED: _ResponseType = {
    status.HTTP_401_UNAUTHORIZED: {"description": "Missing or invalid token"},
}

FORBIDDEN: _ResponseType = {
    status.HTTP_403_FORBIDDEN: {"description": "Insufficient permissions"},
}

NOT_FOUND: _ResponseType = {
    status.HTTP_404_NOT_FOUND: {"description": "Resource not found"},
}

AUTH_RESPONSES: _ResponseType = UNAUTHORIZED | FORBIDDEN
RESOURCE_RESPONSES: _ResponseType = FORBIDDEN | NOT_FOUND
