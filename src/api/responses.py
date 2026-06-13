from fastapi import status

UNAUTHORIZED: dict[int, dict[str, str]] = {
    status.HTTP_401_UNAUTHORIZED: {"description": "Missing or invalid token"},
}

FORBIDDEN: dict[int, dict[str, str]] = {
    status.HTTP_403_FORBIDDEN: {"description": "Insufficient permissions"},
}

NOT_FOUND: dict[int, dict[str, str]] = {
    status.HTTP_404_NOT_FOUND: {"description": "Resource not found"},
}

AUTH_RESPONSES: dict[int, dict[str, str]] = UNAUTHORIZED | FORBIDDEN
RESOURCE_RESPONSES: dict[int, dict[str, str]] = FORBIDDEN | NOT_FOUND
