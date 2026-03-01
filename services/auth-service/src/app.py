from contextlib import asynccontextmanager
from typing import AsyncGenerator, Any

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from dishka.integrations.fastapi import setup_dishka

from api.auth import auth_router
from api.health_check import health_check_router
from core.config import settings
from core.logger import get_logger
from services.metrics import instrumentator
from domain.providers.setup import container
from api.openapi_overrides import apply_bearer_security
from domain.use_cases.seed_admin import SeedAdminUseCase
from infrastructure.postgres.database import PostgresDatabase
from infrastructure.postgres.repositories import UserRepository

logger = get_logger(__name__)


def create_app() -> FastAPI:
    @asynccontextmanager
    async def lifespan_app(app: FastAPI) -> AsyncGenerator[Any, None]:
        try:
            db = PostgresDatabase()
            users = UserRepository()
            seed = SeedAdminUseCase(db, users)
            await seed.execute()
            yield
        finally:
            pass

    app = FastAPI(title="Auth Service", root_path=settings.ROOT_PATH, lifespan=lifespan_app)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth_router, tags=["Auth"])
    app.include_router(health_check_router, tags=["Health Check"])

    instrumentator.instrument(app).expose(app)
    setup_dishka(container, app)
    apply_bearer_security(app)
    return app
