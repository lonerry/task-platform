from fastapi import HTTPException
from starlette import status


class TaskServiceError(Exception):
    pass


class TaskNotFoundError(TaskServiceError):
    def __init__(self, task_id: int) -> None:
        self.message = f"Task with id {task_id} not found"
        super().__init__(self.message)


class DatabaseError(TaskServiceError):
    def __init__(self, detail: str) -> None:
        self.message = detail
        super().__init__(detail)


class KafkaConnectionError(TaskServiceError):
    def __init__(self, detail: str) -> None:
        self.message = detail
        super().__init__(detail)


class TaskValidationError(HTTPException):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=self.message
        )
