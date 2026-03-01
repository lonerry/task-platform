from infrastructure.postgres.database import PostgresDatabase
from infrastructure.postgres.repositories import StatsRepository
from schemas.tasks import TaskStatsResponse


class GetTaskStatsUseCase:
    def __init__(self, db: PostgresDatabase, repo: StatsRepository):
        self.db = db
        self.repo = repo

    async def get_full_stats(self) -> TaskStatsResponse:
        async with self.db.session() as session:
            stats_by_status = await self.repo.get_all_stats(session)
            total_tasks = await self.repo.get_total_tasks(session)
            return TaskStatsResponse(
                total_tasks=total_tasks,
                stats_by_status=stats_by_status,
            )
