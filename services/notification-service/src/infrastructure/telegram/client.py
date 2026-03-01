from __future__ import annotations

import httpx
from core.config import settings
from core.logger import get_logger

logger = get_logger(__name__)


class TelegramClient:
    def __init__(self, bot_token: str, chat_id: str) -> None:
        self._bot_token = bot_token
        self._chat_id = chat_id
        self._base_url = f"https://api.telegram.org/bot{bot_token}"

    async def send_message(self, text: str) -> None:
        if not text:
            return
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(
                f"{self._base_url}/sendMessage",
                json={"chat_id": self._chat_id, "text": text},
            )
        try:
            data = resp.json()
            if not data.get("ok"):
                logger.error("Telegram sendMessage failed: %s", data)
            else:
                logger.info("Telegram message sent, message_id=%s", data.get("result", {}).get("message_id"))
        except Exception as exc:
            logger.error("Failed to parse Telegram response: %s", exc)


def build_telegram_client_from_settings() -> TelegramClient | None:
    if not settings.TELEGRAM_BOT_TOKEN or not settings.TELEGRAM_CHAT_ID:
        return None
    return TelegramClient(settings.TELEGRAM_BOT_TOKEN, settings.TELEGRAM_CHAT_ID)

