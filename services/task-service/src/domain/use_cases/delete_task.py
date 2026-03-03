from core.exceptions.tasks import TaskNotFoundError
from infrastructure.kafka.producer import KafkaProducerService
from infrastructure.postgres.database import PostgresDatabase
from infrastructure.postgres.repositories import TaskRepository


class DeleteTaskUseCase:
    def __init__(
        self, db: PostgresDatabase, repo: TaskRepository, kafka: KafkaProducerService
    ):
        self.db = db
        self.repo = repo
        self.kafka = kafka

    async def execute(self, task_id: int, user_id: int) -> None:
        async with self.db.session() as session:
            task = await self.repo.get_by_id(session, task_id, user_id)
            if task is None:
                raise TaskNotFoundError(task_id)
            try:
                await self.repo.delete(session, task_id, user_id)
            except ValueError:
                raise TaskNotFoundError(task_id)

        await self.kafka.publish_task_deleted(task)
