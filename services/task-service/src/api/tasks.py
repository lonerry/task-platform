from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, HTTPException, Depends
from starlette import status
from core.logger import get_logger, log
from domain.use_cases.create_task import CreateTaskUseCase
from domain.use_cases.get_task import GetTaskUseCase
from domain.use_cases.get_tasks import GetTasksUseCase
from domain.use_cases.update_task import UpdateTaskUseCase
from domain.use_cases.delete_task import DeleteTaskUseCase
from schemas.tasks import Task, CreateTask, UpdateTask
from schemas.pagination import Pagination, PaginationAwareRequest
from core.exceptions.tasks import TaskNotFoundError, TaskValidationError, KafkaConnectionError
from core.security import get_current_user

logger = get_logger(__name__)
tasks_router = APIRouter(prefix="/tasks")


@tasks_router.post("", response_model=Task, status_code=201)
@inject
@log(logger)
async def create_task(payload: CreateTask, use_case: FromDishka[CreateTaskUseCase], current_user=Depends(get_current_user)) -> Task:
    try:
        return await use_case.execute(payload, current_user.id)
    except KafkaConnectionError as e:
        logger.error(e.message)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Service temporarily unavailable")
    except Exception as e:
        logger.exception(f"Unexpected error creating task: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@tasks_router.get("", response_model=Pagination[Task])
@inject
@log(logger)
async def get_tasks(
    use_case: FromDishka[GetTasksUseCase],
    request: PaginationAwareRequest = Depends(),
    current_user=Depends(get_current_user)
) -> Pagination[Task]:
    tasks, total = await use_case.execute(current_user.id, limit=request.limit, offset=request.offset)
    return Pagination(
        limit=request.limit,
        offset=request.offset,
        total=total,
        items=tasks
    )


@tasks_router.get("/{task_id}", response_model=Task)
@inject
@log(logger)
async def get_task(task_id: int, use_case: FromDishka[GetTaskUseCase], current_user=Depends(get_current_user)) -> Task:
    try:
        task = await use_case.execute(task_id, current_user.id)
        if task is None:
            raise TaskNotFoundError(task_id)
        return task
    except TaskNotFoundError as e:
        logger.error(e.message)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except Exception as e:
        logger.exception(f"Unexpected error getting task {task_id}: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@tasks_router.patch("/{task_id}", response_model=Task)
@inject
@log(logger)
async def update_task(task_id: int, payload: UpdateTask, use_case: FromDishka[UpdateTaskUseCase], current_user=Depends(get_current_user)) -> Task:
    try:
        return await use_case.execute(task_id, payload, current_user.id)
    except TaskNotFoundError as e:
        logger.error(e.message)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except KafkaConnectionError as e:
        logger.error(e.message)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Service temporarily unavailable")
    except Exception as e:
        logger.exception(f"Unexpected error updating task {task_id}: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@tasks_router.delete("/{task_id}", status_code=204)
@inject
@log(logger)
async def delete_task(task_id: int, use_case: FromDishka[DeleteTaskUseCase], current_user=Depends(get_current_user)) -> None:
    try:
        await use_case.execute(task_id, current_user.id)
    except TaskNotFoundError as e:
        logger.error(e.message)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except KafkaConnectionError as e:
        logger.error(e.message)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Service temporarily unavailable")
    except Exception as e:
        logger.exception(f"Unexpected error deleting task {task_id}: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
