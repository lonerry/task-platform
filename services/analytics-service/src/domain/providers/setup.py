from dishka import Provider, Scope, provide, make_async_container
from faststream.kafka import KafkaBroker
from infrastructure.postgres.database import PostgresDatabase
from infrastructure.postgres.repositories import StatsRepository
from domain.use_cases.update_stats import UpdateStatsUseCase
from domain.use_cases.get_task_stats import GetTaskStatsUseCase
from core.config import settings


class AppProvider(Provider):
    @provide(scope=Scope.APP)
    async def kafka_broker(self) -> KafkaBroker:
        broker = KafkaBroker(settings.KAFKA_BOOTSTRAP_SERVERS)
        await broker.start()
        return broker

    @provide(scope=Scope.APP)
    async def db(self) -> PostgresDatabase:
        return PostgresDatabase()

    @provide(scope=Scope.REQUEST)
    async def stats_repo(self) -> StatsRepository:
        return StatsRepository()

    @provide(scope=Scope.REQUEST)
    async def update_stats_use_case(self, db: PostgresDatabase, repo: StatsRepository) -> UpdateStatsUseCase:
        return UpdateStatsUseCase(db, repo)

    @provide(scope=Scope.REQUEST)
    async def get_task_stats_use_case(self, db: PostgresDatabase, repo: StatsRepository) -> GetTaskStatsUseCase:
        return GetTaskStatsUseCase(db, repo)


container = make_async_container(AppProvider())
