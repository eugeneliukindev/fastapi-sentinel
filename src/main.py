from contextlib import asynccontextmanager

import jwt
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from src.api.v1 import router as v1_router
from src.exceptions.auth import InvalidCredentialsError, UserAlreadyExistsError
from src.exceptions.rbac import InsufficientPermissionsError
from src.ioc import container


@asynccontextmanager
async def lifespan(app_: FastAPI):
    yield
    await app_.state.dishka_container.close()


app = FastAPI(lifespan=lifespan)
setup_dishka(container, app)
app.include_router(v1_router)


@app.exception_handler(InvalidCredentialsError)
@app.exception_handler(jwt.InvalidTokenError)
async def _on_unauthorized(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": "Invalid credentials"})


@app.exception_handler(UserAlreadyExistsError)
async def _on_conflict(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"detail": "User already exists"})


@app.exception_handler(InsufficientPermissionsError)
async def _on_forbidden(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail": "Forbidden"})
