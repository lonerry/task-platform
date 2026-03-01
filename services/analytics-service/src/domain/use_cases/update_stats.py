from core.logger import get_logger
from infrastructure.postgres.database import PostgresDatabase
from infrastructure.postgres.repositories import StatsRepository

logger = get_logger(__name__)


class UpdateStatsUseCase:
    def __init__(self, db: PostgresDatabase, repo: StatsRepository):
        self.db = db
        self.repo = repo

    async def execute(self, status: str | None):
        if status is None:
            logger.warning("Received task with None status, skipping stats update")
            return

        async with self.db.session() as session:
            await self.repo.update_stats(session, status)

    async def decrement(self, status: str | None):
        if status is None:
            logger.warning("Received task with None status, skipping stats decrement")
            return

        async with self.db.session() as session:
            await self.repo.decrement_stats(session, status)
