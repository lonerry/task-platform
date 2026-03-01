from enum import StrEnum
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class TaskStatus(StrEnum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class CreateTask(BaseModel):
    title: str
    description: str | None = None

class UpdateTask(BaseModel):
    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None

class Task(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    description: str | None
    status: TaskStatus
    user_id: int
    created_at: datetime
    updated_at: datetime