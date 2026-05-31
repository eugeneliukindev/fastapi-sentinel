from contextlib import asynccontextmanager

from dishka.integrations.fastapi import DishkaRoute, setup_dishka
from fastapi import APIRouter, FastAPI

from src.ioc import container


@asynccontextmanager
async def lifespan(app_: FastAPI):
    yield
    # On shutdown, close the dishka container: this finalizes all APP-scoped
    # resources in reverse creation order, running the teardown after `yield` in
    # each generator provider (e.g. AsyncEngine.dispose()).
    await app_.state.dishka_container.close()


app = FastAPI(lifespan=lifespan)
router = APIRouter(route_class=DishkaRoute)


setup_dishka(container, app)

app.include_router(router)
