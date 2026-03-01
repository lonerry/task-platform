from datetime import datetime, timedelta, timezone
from typing import Any, Dict

import jwt
from passlib.context import CryptContext

from core.config import settings


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return password_context.verify(password, password_hash)


def _create_token(data: Dict[str, Any], expires_delta: timedelta) -> str:
    payload = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    payload.update({"exp": expire, "iat": datetime.now(timezone.utc)})
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)


def create_access_token(sub: str, role: str) -> str:
    return _create_token({"sub": sub, "role": role, "type": "access"}, timedelta(seconds=settings.ACCESS_TOKEN_TTL))


def create_refresh_token(sub: str) -> str:
    return _create_token({"sub": sub, "type": "refresh"}, timedelta(seconds=settings.REFRESH_TOKEN_TTL))


def decode_token(token: str) -> Dict[str, Any]:
    return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])


