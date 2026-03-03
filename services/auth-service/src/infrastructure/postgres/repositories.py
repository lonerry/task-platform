from datetime import datetime
from typing import Optional

from core.logger import get_logger, log
from infrastructure.postgres.models import RefreshTokenModel, UserModel
from schemas.auth import (CreateRefreshToken, CreateUser, RefreshToken, User,
                          UserWithPassword)
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

logger = get_logger(__name__)


class UserRepository:
    @log(logger)
    async def create(self, session: AsyncSession, user: CreateUser) -> User:
        query = insert(UserModel).values(**user.model_dump()).returning(UserModel)
        result = await session.scalar(query)
        return User.model_validate(result)

    @log(logger)
    async def get_by_email(
        self, session: AsyncSession, email: str
    ) -> Optional[UserWithPassword]:
        query = select(UserModel).where(UserModel.email == email)
        result = await session.execute(query)
        obj = result.scalar_one_or_none()
        return UserWithPassword.model_validate(obj) if obj else None

    @log(logger)
    async def get_by_id(self, session: AsyncSession, user_id: int) -> Optional[User]:
        query = select(UserModel).where(UserModel.id == user_id)
        result = await session.execute(query)
        obj = result.scalar_one_or_none()
        return User.model_validate(obj) if obj else None

    @log(logger)
    async def update_role(self, session: AsyncSession, user_id: int, role: str) -> User:
        query = (
            update(UserModel)
            .where(UserModel.id == user_id)
            .values(role=role)
            .returning(UserModel)
        )
        result = await session.execute(query)
        obj = result.scalar_one_or_none()
        if obj is None:
            raise ValueError(f"UserModel with id {user_id} not found")
        return User.model_validate(obj)


class RefreshTokenRepository:
    @log(logger)
    async def create(
        self, session: AsyncSession, token: CreateRefreshToken
    ) -> RefreshToken:
        query = (
            insert(RefreshTokenModel)
            .values(**token.model_dump())
            .returning(RefreshTokenModel)
        )
        result = await session.scalar(query)
        return RefreshToken.model_validate(result)

    @log(logger)
    async def get(self, session: AsyncSession, token: str) -> Optional[RefreshToken]:
        query = select(RefreshTokenModel).where(RefreshTokenModel.token == token)
        result = await session.execute(query)
        obj = result.scalar_one_or_none()
        return RefreshToken.model_validate(obj) if obj else None

    @log(logger)
    async def delete(self, session: AsyncSession, token: str) -> None:
        query = delete(RefreshTokenModel).where(RefreshTokenModel.token == token)
        await session.execute(query)

    @log(logger)
    async def delete_expired(self, session: AsyncSession, now: datetime) -> int:
        query = delete(RefreshTokenModel).where(RefreshTokenModel.expires_at < now)
        result = await session.execute(query)
        return result.rowcount or 0
