from enum import StrEnum
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class TaskStatus(StrEnum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Task(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int | None
    title: str | None
    description: str | None
    status: str | None
    created_at: datetime | None
    updated_at: datetime | None


class TaskStats(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    status: str
    count: int
    updated_at: datetime


class TaskStatsResponse(BaseModel):
    """Ответ API с общей статистикой"""
    total_tasks: int
    stats_by_status: list[TaskStats]
