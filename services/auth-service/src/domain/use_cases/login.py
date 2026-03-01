from datetime import datetime, timedelta, timezone

from infrastructure.postgres.database import PostgresDatabase
from infrastructure.postgres.repositories import UserRepository, RefreshTokenRepository
from services.security import verify_password, create_access_token, create_refresh_token
from schemas.auth import TokenPair, CreateRefreshToken, UserWithPassword
from core.config import settings


class LoginUseCase:
    def __init__(self, db: PostgresDatabase, user_repo: UserRepository, refresh_repo: RefreshTokenRepository) -> None:
        self._db = db
        self._users = user_repo
        self._refresh = refresh_repo

    async def execute(self, email: str, password: str) -> TokenPair:
        async with self._db.session() as session:
            user: UserWithPassword | None = await self._users.get_by_email(session, email)
            if not user or not verify_password(password, user.password_hash):
                raise ValueError("Invalid credentials")

            access = create_access_token(str(user.id), user.role)
            refresh = create_refresh_token(str(user.id))
            expires_at = datetime.now(timezone.utc) + timedelta(seconds=settings.REFRESH_TOKEN_TTL)
            await self._refresh.create(session, CreateRefreshToken(user_id=user.id, token=refresh, expires_at=expires_at))

            return TokenPair(access_token=access, refresh_token=refresh, expires_in=settings.ACCESS_TOKEN_TTL)


