from core.logger import get_logger
from infrastructure.postgres.database import PostgresDatabase
from infrastructure.postgres.repositories import TaskRepository
from schemas.tasks import Task, CreateTask
from infrastructure.kafka.producer import KafkaProducerService

logger = get_logger(__name__)


class CreateTaskUseCase:
    def __init__(self, db: PostgresDatabase, repo: TaskRepository, kafka: KafkaProducerService):
        self.db = db
        self.repo = repo
        self.kafka = kafka

    async def execute(self, task: CreateTask, user_id: int) -> Task:
        async with self.db.session() as session:
            created_task = await self.repo.create(session, task, user_id)

        await self.kafka.publish_task_created(created_task)
        return created_task
