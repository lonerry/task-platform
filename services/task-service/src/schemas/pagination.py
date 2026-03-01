from typing import Generic, List, TypeVar

from fastapi import Query
from pydantic import BaseModel, Field


class PaginationAwareRequest(BaseModel):
    limit: int = Query(100, description="Количество элементов на странице")
    offset: int = Query(0, description="Смещение от начала")


T = TypeVar("T")


class Pagination(BaseModel, Generic[T]):
    """
    Модель пагинации
    Обертка для списка элементов с информацией о пагинации
    """

    limit: int = 10
    offset: int = 0
    count: int = 0  # количество элементов на странице
    total: int = 0  # общее количество элементов
    items: List[T] = Field(default_factory=list)

    def __init__(self, **data) -> None:  # type: ignore
        data.setdefault("count", len(data.get("items", [])))
        super().__init__(**data)

