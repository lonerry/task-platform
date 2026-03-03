from infrastructure.postgres.database import PostgresDatabase
from infrastructure.postgres.repositories import TaskRepository
from schemas.tasks import Task


class GetTaskUseCase:
    def __init__(self, db: PostgresDatabase, repo: TaskRepository):
        self.db = db
        self.repo = repo

    async def execute(self, task_id: int, user_id: int) -> Task | None:
        async with self.db.session() as session:
            return await self.repo.get_by_id(session, task_id, user_id)
