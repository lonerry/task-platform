from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    LOG_LEVEL: str = "INFO"
    ORIGINS: str | list[str] = "*"
    PORT: int = 8000
    ROOT_PATH: str = ""
    ENV: str = "DEV"

    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "postgres"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_SCHEMA: str = "analytics"
    MIN_POOL_SIZE: int = 5
    MAX_POOL_SIZE: int = 20
    POSTGRES_POOL_PRE_PING: bool = True

    KAFKA_BOOTSTRAP_SERVERS: str = "kafka:9092"
    KAFKA_TOPIC: str = "tasks"

    @field_validator("ORIGINS")
    def _process_origins(cls, value: str) -> list[str]:
        return [origin.strip() for origin in value.split(",")]

    @property
    def postgres_url(self) -> str:
        creds = f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
        return f"postgresql+asyncpg://{creds}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


settings = Settings()
