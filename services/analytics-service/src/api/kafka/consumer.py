from dishka.integrations.faststream import inject
from faststream.kafka import KafkaBroker, KafkaRouter

from core.config import settings
from dishka import FromDishka
from domain.use_cases.update_stats import UpdateStatsUseCase
from schemas.tasks import Task

router = KafkaRouter()
broker = KafkaBroker(settings.KAFKA_BOOTSTRAP_SERVERS)


@router.subscriber(f"{settings.KAFKA_TOPIC}_created", group_id="analytics-service")
@inject
async def handle_task_created(msg: bytes, use_case: FromDishka[UpdateStatsUseCase]) -> None:
    task = Task.model_validate_json(msg)
    await use_case.execute(task.status)


@router.subscriber(f"{settings.KAFKA_TOPIC}_updated", group_id="analytics-service")
@inject
async def handle_task_updated(msg: bytes, use_case: FromDishka[UpdateStatsUseCase]) -> None:
    task = Task.model_validate_json(msg)
    await use_case.execute(task.status)


@router.subscriber(f"{settings.KAFKA_TOPIC}_deleted", group_id="analytics-service")
@inject
async def handle_task_deleted(msg: bytes, use_case: FromDishka[UpdateStatsUseCase]) -> None:
    task = Task.model_validate_json(msg)
    await use_case.decrement(task.status)
