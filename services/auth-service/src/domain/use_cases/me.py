from infrastructure.postgres.database import PostgresDatabase
from infrastructure.postgres.repositories import UserRepository
from schemas.auth import MeResponse
from services.security import decode_token


class MeUseCase:
    def __init__(self, db: PostgresDatabase, user_repo: UserRepository) -> None:
        self._db = db
        self._users = user_repo

    async def execute(self, access_token: str) -> MeResponse:
        payload = decode_token(access_token)
        if payload.get("type") != "access":
            raise ValueError("Invalid token type")
        user_id = int(payload["sub"])
        async with self._db.session() as session:
            user = await self._users.get_by_id(session, user_id)
            if user is None:
                raise ValueError("User not found")
            return MeResponse(
                id=user.id, email=user.email, role=user.role, is_active=user.is_active
            )
