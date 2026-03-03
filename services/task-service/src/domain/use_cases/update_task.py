from core.exceptions.tasks import TaskNotFoundError
from infrastructure.kafka.producer import KafkaProducerService
from infrastructure.postgres.database import PostgresDatabase
from infrastructure.postgres.repositories import TaskRepository
from schemas.tasks import Task, UpdateTask


class UpdateTaskUseCase:
    def __init__(
        self, db: PostgresDatabase, repo: TaskRepository, kafka: KafkaProducerService
    ):
        self.db = db
        self.repo = repo
        self.kafka = kafka

    async def execute(self, task_id: int, task: UpdateTask, user_id: int) -> Task:
        async with self.db.session() as session:
            try:
                updated_task = await self.repo.update(session, task_id, task, user_id)
            except ValueError:
                raise TaskNotFoundError(task_id)

        await self.kafka.publish_task_updated(updated_task)
        return updated_task
