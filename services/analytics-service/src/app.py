from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from api.health_check import health_check_router
from api.kafka.consumer import broker, router
from api.task_stats import task_stats_router
from core.config import settings
from core.logger import get_logger
from dishka.integrations.fastapi import setup_dishka
from dishka.integrations.faststream import \
    setup_dishka as setup_dishka_faststream
from domain.providers.setup import container
from fastapi import FastAPI
from faststream import FastStream
from services.metrics import instrumentator
from starlette.middleware.cors import CORSMiddleware

logger = get_logger(__name__)


def create_app() -> FastAPI:
    @asynccontextmanager
    async def lifespan_app(app: FastAPI) -> AsyncGenerator[Any, None]:
        try:
            logger.info("Starting Kafka broker")
            await broker.start()
            logger.info("Kafka broker started")
            yield
        except Exception as e:
            logger.error(f"Failed to start application: {e}")
            raise
        finally:
            logger.info("Shutting down application")
            await broker.close()
            await app.state.dishka_container.close()

    app = FastAPI(
        title="Analytics Service", root_path=settings.ROOT_PATH, lifespan=lifespan_app
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health_check_router, tags=["Health Check"])
    app.include_router(task_stats_router, tags=["Task Statistics"])

    instrumentator.instrument(app).expose(app)
    setup_dishka(container, app)
    broker.include_router(router=router)
    setup_dishka_faststream(container, FastStream(broker))

    return app
