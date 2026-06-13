from collections.abc import Callable, Coroutine
from typing import Any, TypeAlias

import jwt
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from src.exceptions.auth import InvalidCredentialsError, UserAlreadyExistsError
from src.exceptions.rbac import InsufficientPermissionsError, RoleAlreadyAssignedError
from src.exceptions.user import UserNotFoundError

_HandlerType: TypeAlias = Callable[..., Coroutine[Any, Any, Any]]


async def _on_unauthorized(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": "Invalid credentials"})


async def _on_conflict(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"detail": str(exc)})


async def _on_forbidden(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail": "Forbidden"})


async def _on_not_found(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": "User not found"})


_HANDLERS: dict[_HandlerType, tuple[type[Exception], ...]] = {
    _on_unauthorized: (InvalidCredentialsError, jwt.InvalidTokenError),
    _on_conflict: (UserAlreadyExistsError, RoleAlreadyAssignedError),
    _on_forbidden: (InsufficientPermissionsError,),
    _on_not_found: (UserNotFoundError,),
}


def setup_exception_handlers(app: FastAPI) -> None:
    for handler, exc_classes in _HANDLERS.items():
        for exc_class in exc_classes:
            app.add_exception_handler(exc_class, handler)
