from dishka import Provider, Scope, provide, make_async_container
from faststream.kafka import KafkaBroker
from core.config import settings
from infrastructure.postgres.database import PostgresDatabase
from infrastructure.postgres.repositories import TaskRepository
from infrastructure.kafka.producer import KafkaProducerService
from domain.use_cases.create_task import CreateTaskUseCase
from domain.use_cases.get_task import GetTaskUseCase
from domain.use_cases.get_tasks import GetTasksUseCase
from domain.use_cases.update_task import UpdateTaskUseCase
from domain.use_cases.delete_task import DeleteTaskUseCase


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
    async def task_repo(self) -> TaskRepository:
        return TaskRepository()

    @provide(scope=Scope.REQUEST)
    async def kafka_producer(self, broker: KafkaBroker) -> KafkaProducerService:
        return KafkaProducerService(broker)

    @provide(scope=Scope.REQUEST)
    async def create_task_use_case(self, db: PostgresDatabase, repo: TaskRepository,
                                   kafka: KafkaProducerService) -> CreateTaskUseCase:
        return CreateTaskUseCase(db, repo, kafka)

    @provide(scope=Scope.REQUEST)
    async def get_task_use_case(self, db: PostgresDatabase, repo: TaskRepository) -> GetTaskUseCase:
        return GetTaskUseCase(db, repo)

    @provide(scope=Scope.REQUEST)
    async def get_tasks_use_case(self, db: PostgresDatabase, repo: TaskRepository) -> GetTasksUseCase:
        return GetTasksUseCase(db, repo)

    @provide(scope=Scope.REQUEST)
    async def update_task_use_case(self, db: PostgresDatabase, repo: TaskRepository,
                                   kafka: KafkaProducerService) -> UpdateTaskUseCase:
        return UpdateTaskUseCase(db, repo, kafka)

    @provide(scope=Scope.REQUEST)
    async def delete_task_use_case(self, db: PostgresDatabase, repo: TaskRepository,
                                   kafka: KafkaProducerService) -> DeleteTaskUseCase:
        return DeleteTaskUseCase(db, repo, kafka)


container = make_async_container(AppProvider())
