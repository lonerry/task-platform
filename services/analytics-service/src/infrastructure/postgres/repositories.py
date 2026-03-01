from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, func
from core.logger import get_logger, log
from schemas.tasks import TaskStatus, TaskStats as TaskStatsSchema
from infrastructure.postgres.models import TaskStats
from typing import List

logger = get_logger(__name__)


class StatsRepository:
    @log(logger)
    async def update_stats(self, session: AsyncSession, status: str):
        query = select(TaskStats).where(TaskStats.status == status)
        result = await session.execute(query)
        stats = result.scalar_one_or_none()

        if stats:
            query = update(TaskStats).where(TaskStats.status == status).values(count=TaskStats.count + 1)
            operation = "increment"
        else:
            query = insert(TaskStats).values(status=status, count=1)
            operation = "create"

        await session.execute(query)
        logger.info(f"Stats {operation} for status '{status}'")

    @log(logger)
    async def decrement_stats(self, session: AsyncSession, status: str):
        query = select(TaskStats).where(TaskStats.status == status)
        result = await session.execute(query)
        stats = result.scalar_one_or_none()

        if stats and stats.count > 0:
            query = update(TaskStats).where(TaskStats.status == status).values(count=TaskStats.count - 1)
            await session.execute(query)
            logger.info(f"Stats decrement for status '{status}'")

    @log(logger)
    async def get_all_stats(self, session: AsyncSession) -> List[TaskStatsSchema]:
        query = select(TaskStats).order_by(TaskStats.status)
        result = await session.execute(query)
        stats = result.scalars().all()
        return [TaskStatsSchema.model_validate(stat) for stat in stats]

    @log(logger)
    async def get_stats_by_status(self, session: AsyncSession, status: str) -> TaskStatsSchema | None:
        query = select(TaskStats).where(TaskStats.status == status)
        result = await session.execute(query)
        stat = result.scalar_one_or_none()
        return TaskStatsSchema.model_validate(stat) if stat else None

    @log(logger)
    async def get_total_tasks(self, session: AsyncSession) -> int:
        query = select(func.sum(TaskStats.count))
        result = await session.execute(query)
        total = result.scalar()
        return total if total is not None else 0
