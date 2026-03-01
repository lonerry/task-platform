from infrastructure.postgres.database import PostgresDatabase
from infrastructure.postgres.repositories import UserRepository
from services.security import hash_password
from core.config import settings
from schemas.auth import CreateUser


class SeedAdminUseCase:
    def __init__(self, db: PostgresDatabase, user_repo: UserRepository) -> None:
        self._db = db
        self._users = user_repo

    async def execute(self) -> None:
        async with self._db.session() as session:
            existing = await self._users.get_by_email(session, settings.ADMIN_EMAIL)
            if existing:
                return
            await self._users.create(
                session,
                CreateUser(
                    email=settings.ADMIN_EMAIL,
                    password_hash=hash_password(settings.ADMIN_PASSWORD),
                    role="admin",
                ),
            )


