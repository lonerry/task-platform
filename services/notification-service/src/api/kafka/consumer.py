from core.config import settings
from dishka import FromDishka
from dishka.integrations.faststream import inject
from faststream.kafka import KafkaBroker, KafkaRouter
from schemas.tasks import Task
from services.notification import NotificationService

router = KafkaRouter()
broker = KafkaBroker(settings.KAFKA_BOOTSTRAP_SERVERS)


@router.subscriber(f"{settings.KAFKA_TOPIC}_created", group_id="notification-service")
@inject
async def handle_task_created(
    msg: bytes, service: FromDishka[NotificationService]
) -> None:
    task = Task.model_validate_json(msg)
    await service.send_telegram_created(task)


@router.subscriber(f"{settings.KAFKA_TOPIC}_updated", group_id="notification-service")
@inject
async def handle_task_updated(
    msg: bytes, service: FromDishka[NotificationService]
) -> None:
    task = Task.model_validate_json(msg)
    await service.send_telegram_updated(task)


@router.subscriber(f"{settings.KAFKA_TOPIC}_deleted", group_id="notification-service")
@inject
async def handle_task_deleted(
    msg: bytes, service: FromDishka[NotificationService]
) -> None:
    task = Task.model_validate_json(msg)
    await service.send_telegram_deleted(task.id)
