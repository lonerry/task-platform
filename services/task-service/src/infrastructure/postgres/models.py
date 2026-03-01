from sqlalchemy import String, DateTime, Integer, Enum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from core.config import settings
from infrastructure.postgres.base import Base
from schemas.tasks import TaskStatus


class TaskModel(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=False, server_default=TaskStatus.NEW)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(),
                                                 nullable=False)