from dishka import Provider, Scope, make_async_container, provide

from infrastructure.telegram.client import build_telegram_client_from_settings
from services.notification import NotificationService


class AppProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def notification_service(self) -> NotificationService:
        telegram_client = build_telegram_client_from_settings()
        return NotificationService(message_sender=telegram_client)


container = make_async_container(AppProvider())
