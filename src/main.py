from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from src.api import router as api_router
from src.api.exception_handlers import setup_exception_handlers
from src.ioc import container


@asynccontextmanager
async def lifespan(app_: FastAPI) -> AsyncGenerator[None]:
    yield
    await app_.state.dishka_container.close()


app = FastAPI(lifespan=lifespan)
setup_dishka(container, app)
setup_exception_handlers(app)
app.include_router(api_router)
