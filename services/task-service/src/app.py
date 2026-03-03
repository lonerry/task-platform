from api.health_check import health_check_router
from api.tasks import tasks_router
from core.config import settings
from core.logger import get_logger
from dishka.integrations.fastapi import setup_dishka
from domain.providers.setup import container
from fastapi import FastAPI
from services.metrics import instrumentator
from starlette.middleware.cors import CORSMiddleware

logger = get_logger(__name__)


def create_app() -> FastAPI:
    app = FastAPI(title="Task Service", root_path=settings.ROOT_PATH)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(tasks_router, tags=["Tasks"])
    app.include_router(health_check_router, tags=["Health Check"])

    instrumentator.instrument(app).expose(app)
    setup_dishka(container, app)
    return app
