from core.config import settings
from core.logger import get_logger
from faststream.kafka import KafkaBroker
from schemas.tasks import Task

logger = get_logger(__name__)


class KafkaProducerService:
    def __init__(self, broker: KafkaBroker):
        self.broker = broker

    async def publish_task_created(self, task: Task):
        try:
            await self.broker.publish(
                message=task.model_dump_json(),
                topic=f"{settings.KAFKA_TOPIC}_created",
                key=str(task.id).encode(),
            )
            logger.info(f"Published task creation event for task {task.id}")
        except Exception as e:
            logger.error(
                f"Failed to publish task creation event for task {task.id}: {e}"
            )
            raise

    async def publish_task_updated(self, task: Task):
        try:
            await self.broker.publish(
                message=task.model_dump_json(),
                topic=f"{settings.KAFKA_TOPIC}_updated",
                key=str(task.id).encode(),
            )
            logger.info(f"Published task update event for task {task.id}")
        except Exception as e:
            logger.error(f"Failed to publish task update event for task {task.id}: {e}")
            raise

    async def publish_task_deleted(self, task: Task):
        try:
            await self.broker.publish(
                message=task.model_dump_json(),
                topic=f"{settings.KAFKA_TOPIC}_deleted",
                key=str(task.id).encode(),
            )
            logger.info(f"Published task deletion event for task {task.id}")
        except Exception as e:
            logger.error(
                f"Failed to publish task deletion event for task {task.id}: {e}"
            )
            raise
