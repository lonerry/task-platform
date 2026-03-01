from datetime import datetime, timedelta, timezone
from infrastructure.postgres.database import PostgresDatabase
from infrastructure.postgres.repositories import UserRepository, RefreshTokenRepository
from services.security import create_access_token, decode_token
from schemas.auth import TokenPair
from core.config import settings


class RefreshUseCase:
    def __init__(self, db: PostgresDatabase, user_repo: UserRepository, refresh_repo: RefreshTokenRepository) -> None:
        self._db = db
        self._users = user_repo
        self._refresh = refresh_repo

    async def execute(self, refresh_token: str) -> TokenPair:
        async with self._db.session() as session:
            stored = await self._refresh.get(session, refresh_token)
            if stored is None or stored.expires_at < datetime.now(timezone.utc):
                raise ValueError("Invalid refresh token")

            payload = decode_token(refresh_token)
            if payload.get("type") != "refresh":
                raise ValueError("Invalid token type")

            user_id = int(payload["sub"])
            user = await self._users.get_by_id(session, user_id)
            if user is None:
                raise ValueError("User not found")

            access = create_access_token(str(user.id), user.role)
            return TokenPair(access_token=access, refresh_token=refresh_token, expires_in=settings.ACCESS_TOKEN_TTL)


