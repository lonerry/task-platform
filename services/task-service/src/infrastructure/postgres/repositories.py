from core.logger import get_logger, log
from infrastructure.postgres.models import TaskModel
from schemas.tasks import CreateTask, Task, UpdateTask
from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

logger = get_logger(__name__)


class TaskRepository:
    @log(logger)
    async def create(
        self, session: AsyncSession, task: CreateTask, user_id: int
    ) -> Task:
        task_data = task.model_dump()
        task_data["user_id"] = user_id
        query = insert(TaskModel).values(**task_data).returning(TaskModel)
        result = await session.scalar(query)
        return Task.model_validate(result)

    @log(logger)
    async def get_by_id(
        self, session: AsyncSession, task_id: int, user_id: int
    ) -> Task | None:
        query = select(TaskModel).where(
            TaskModel.id == task_id, TaskModel.user_id == user_id
        )
        result = await session.execute(query)
        task = result.scalar_one_or_none()
        return Task.model_validate(task) if task else None

    @log(logger)
    async def get_all(
        self, session: AsyncSession, user_id: int, limit: int = 100, offset: int = 0
    ) -> list[Task]:
        query = (
            select(TaskModel)
            .where(TaskModel.user_id == user_id)
            .limit(limit)
            .offset(offset)
            .order_by(TaskModel.created_at.desc())
        )
        result = await session.execute(query)
        tasks = result.scalars().all()
        return [Task.model_validate(task) for task in tasks]

    @log(logger)
    async def count_all(self, session: AsyncSession, user_id: int) -> int:
        query = select(func.count(TaskModel.id)).where(TaskModel.user_id == user_id)
        result = await session.scalar(query)
        return result or 0

    @log(logger)
    async def count_by_status(self, session: AsyncSession) -> dict[str, int]:
        query = select(TaskModel.status, func.count(TaskModel.id)).group_by(
            TaskModel.status
        )
        result = await session.execute(query)
        return dict(result.all())

    @log(logger)
    async def update(
        self, session: AsyncSession, task_id: int, task: UpdateTask, user_id: int
    ) -> Task:
        query = (
            update(TaskModel)
            .where(TaskModel.id == task_id, TaskModel.user_id == user_id)
            .values(**task.model_dump())
            .returning(TaskModel)
        )
        result = await session.execute(query)
        task = result.scalar_one_or_none()
        if task is None:
            raise ValueError(f"TaskModel with id {task_id} not found")
        return Task.model_validate(task)

    @log(logger)
    async def delete(self, session: AsyncSession, task_id: int, user_id: int) -> None:
        query = delete(TaskModel).where(
            TaskModel.id == task_id, TaskModel.user_id == user_id
        )
        result = await session.execute(query)
        if result.rowcount == 0:
            raise ValueError(f"TaskModel with id {task_id} not found")
