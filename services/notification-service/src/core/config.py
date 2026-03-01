from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    LOG_LEVEL: str = "INFO"
    ORIGINS: str | list[str] = "*"
    PORT: int = 8000
    ROOT_PATH: str = ""
    ENV: str = "DEV"

    KAFKA_BOOTSTRAP_SERVERS: str
    KAFKA_TOPIC: str = "tasks"

    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_CHAT_ID: str

    @field_validator("ORIGINS")
    def _process_origins(cls, value: str) -> list[str]:
        return [origin.strip() for origin in value.split(",")]


settings = Settings()
