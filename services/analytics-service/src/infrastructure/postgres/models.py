from sqlalchemy import Integer, Enum, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from schemas.tasks import TaskStatus
from infrastructure.postgres.database import Base


class TaskStats(Base):
    __tablename__ = "task_stats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    status: Mapped[str] = mapped_column(String)
    count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(),
                                                 nullable=False)