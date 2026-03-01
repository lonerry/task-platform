from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter
from domain.use_cases.get_task_stats import GetTaskStatsUseCase
from schemas.tasks import TaskStatsResponse

task_stats_router = APIRouter(prefix="/task-stats")


@task_stats_router.get("", response_model=TaskStatsResponse)
@inject
async def get_task_stats(use_case: FromDishka[GetTaskStatsUseCase]) -> TaskStatsResponse:
    return await use_case.get_full_stats()
