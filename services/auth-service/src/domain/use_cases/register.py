from dishka import Provider
from infrastructure.postgres.database import PostgresDatabase
from infrastructure.postgres.repositories import UserRepository
from services.security import hash_password
from schemas.auth import MeResponse, CreateUser


class RegisterUseCase:
    def __init__(self, db: PostgresDatabase, user_repo: UserRepository) -> None:
        self._db = db
        self._users = user_repo

    async def execute(self, email: str, password: str) -> MeResponse:
        async with self._db.session() as session:
            existing = await self._users.get_by_email(session, email)
            if existing:
                raise ValueError("User already exists")
            user = await self._users.create(session, CreateUser(email=email, password_hash=hash_password(password)))
            return MeResponse(id=user.id, email=user.email, role=user.role, is_active=user.is_active)


