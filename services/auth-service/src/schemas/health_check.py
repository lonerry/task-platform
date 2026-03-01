from pydantic import BaseModel


class HealthStatus(BaseModel):
    postgres: bool


