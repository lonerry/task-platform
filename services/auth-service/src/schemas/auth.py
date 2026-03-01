from datetime import datetime
from typing import Generic, Optional, TypeVar

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


class CreateUser(BaseModel):
    email: EmailStr
    password_hash: str
    role: str = "user"
    is_active: bool = True


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class RefreshRequest(BaseModel):
    refresh_token: str


class RefreshToken(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    token: str
    expires_at: datetime
    created_at: datetime


class CreateRefreshToken(BaseModel):
    user_id: int
    token: str
    expires_at: datetime


class UserWithPassword(User):
    password_hash: str


class AssignRoleRequest(BaseModel):
    user_id: int
    role: str = Field(pattern="^(admin|moderator|user)$")


class MeResponse(BaseModel):
    id: int
    email: EmailStr
    role: str
    is_active: bool


