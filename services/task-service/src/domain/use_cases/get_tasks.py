from infrastructure.postgres.database import PostgresDatabase
from infrastructure.postgres.repositories import TaskRepository
from schemas.tasks import Task


class GetTasksUseCase:
    def __init__(self, db: PostgresDatabase, repo: TaskRepository):
        self.db = db
        self.repo = repo

    async def execute(
        self, user_id: int, limit: int = 100, offset: int = 0
    ) -> tuple[list[Task], int]:
        async with self.db.session() as session:
            tasks = await self.repo.get_all(
                session, user_id, limit=limit, offset=offset
            )
            total_count = await self.repo.count_all(session, user_id)
            return tasks, total_count
