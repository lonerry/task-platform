from contextlib import asynccontextmanager

from dishka.integrations.fastapi import setup_dishka
from dishka.integrations.faststream import setup_dishka as setup_dishka_faststream
from fastapi import FastAPI
from faststream import FastStream
from starlette.middleware.cors import CORSMiddleware

from api.health_check import health_check_router
from core.config import settings
from core.logger import get_logger
from domain.providers.setup import container
from services.metrics import instrumentator
from api.kafka.consumer import broker, router

logger = get_logger(__name__)


def create_app() -> FastAPI:
    @asynccontextmanager
    async def lifespan_app(app: FastAPI):
        try:
            logger.info("Starting Kafka broker")
            await broker.start()
            logger.info("Kafka broker started")
            yield
        finally:
            logger.info("Shutting down application")
            await broker.close()
            await app.state.dishka_container.close()

    app = FastAPI(
        title="Notification Service",
        root_path=settings.ROOT_PATH,
        docs_url=None if settings.ENV == "PROD" else "/docs",
        redoc_url=None if settings.ENV == "PROD" else "/redoc",
        lifespan=lifespan_app,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(health_check_router, tags=["Health Check"])

    instrumentator.instrument(app).expose(app)
    setup_dishka(container, app)
    broker.include_router(router=router)
    setup_dishka_faststream(container, FastStream(broker))

    return app
