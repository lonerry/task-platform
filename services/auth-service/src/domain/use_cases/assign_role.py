from infrastructure.postgres.database import PostgresDatabase
from infrastructure.postgres.repositories import UserRepository
from services.security import decode_token
from schemas.auth import MeResponse


class AssignRoleUseCase:
    def __init__(self, db: PostgresDatabase, user_repo: UserRepository) -> None:
        self._db = db
        self._users = user_repo

    async def execute(self, access_token: str, user_id: int, role: str) -> MeResponse:
        payload = decode_token(access_token)
        if payload.get("type") != "access":
            raise ValueError("Invalid token type")
        if payload.get("role") != "admin":
            raise PermissionError("Only admin can assign roles")

        async with self._db.session() as session:
            updated = await self._users.update_role(session, user_id, role)
            return MeResponse(id=updated.id, email=updated.email, role=updated.role, is_active=updated.is_active)


