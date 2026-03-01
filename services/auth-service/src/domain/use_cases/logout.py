from infrastructure.postgres.database import PostgresDatabase
from infrastructure.postgres.repositories import RefreshTokenRepository


class LogoutUseCase:
    def __init__(self, db: PostgresDatabase, refresh_repo: RefreshTokenRepository) -> None:
        self._db = db
        self._refresh = refresh_repo

    async def execute(self, refresh_token: str) -> None:
        async with self._db.session() as session:
            await self._refresh.delete(session, refresh_token)


