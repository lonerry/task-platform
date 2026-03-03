from typing import Protocol

from core.logger import get_logger
from schemas.tasks import Task


class MessageSender(Protocol):
    async def send_message(self, text: str) -> None: ...


logger = get_logger(__name__)


class NotificationService:
    def __init__(self, message_sender: MessageSender | None = None):
        self.message_sender = message_sender

    async def send_telegram_created(self, task: Task) -> None:
        if not self.message_sender:
            return
        text = (
            f"Новая задача #{task.id}\n"
            f"Название: {task.title}\n"
            f"Статус: {task.status}\n"
            f"Создана: {task.created_at:%Y-%m-%d %H:%M:%S}"
        )
        await self.message_sender.send_message(text)

    async def send_telegram_updated(self, task: Task) -> None:
        if not self.message_sender:
            return
        text = (
            f"Обновлена задача #{task.id}\n"
            f"Название: {task.title}\n"
            f"Статус: {task.status}"
        )
        await self.message_sender.send_message(text)

    async def send_telegram_deleted(self, task_id: int) -> None:
        if not self.message_sender:
            return
        text = f"Задача #{task_id} удалена"
        await self.message_sender.send_message(text)
