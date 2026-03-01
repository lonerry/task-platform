from typing import Annotated

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette import status

from core.logger import get_logger, log
from domain.use_cases.assign_role import AssignRoleUseCase
from domain.use_cases.login import LoginUseCase
from domain.use_cases.logout import LogoutUseCase
from domain.use_cases.me import MeUseCase
from domain.use_cases.refresh import RefreshUseCase
from domain.use_cases.register import RegisterUseCase
from schemas.auth import LoginRequest, TokenPair, RefreshRequest, MeResponse, AssignRoleRequest


logger = get_logger(__name__)
auth_router = APIRouter(prefix="/auth")
bearer_scheme = HTTPBearer(auto_error=False)


@auth_router.post("/register", response_model=MeResponse, status_code=201)
@inject
@log(logger)
async def register(payload: LoginRequest, use_case: FromDishka[RegisterUseCase]) -> MeResponse:
    try:
        return await use_case.execute(payload.email, payload.password)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@auth_router.post("/login", response_model=TokenPair)
@inject
@log(logger)
async def login(payload: LoginRequest, use_case: FromDishka[LoginUseCase]) -> TokenPair:
    try:
        return await use_case.execute(payload.email, payload.password)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@auth_router.post("/refresh", response_model=TokenPair)
@inject
@log(logger)
async def refresh(payload: RefreshRequest, use_case: FromDishka[RefreshUseCase]) -> TokenPair:
    try:
        return await use_case.execute(payload.refresh_token)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@auth_router.post("/logout", status_code=204)
@inject
@log(logger)
async def logout(payload: RefreshRequest, use_case: FromDishka[LogoutUseCase]) -> None:
    await use_case.execute(payload.refresh_token)


def get_current_token(credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)]) -> str:
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return credentials.credentials


@auth_router.get("/me", response_model=MeResponse)
@inject
@log(logger)
async def me(
    use_case: FromDishka[MeUseCase],
    token: str = Depends(get_current_token),
) -> MeResponse:
    try:
        return await use_case.execute(token)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@auth_router.post("/assign-role", response_model=MeResponse)
@inject
@log(logger)
async def assign_role(
    payload: AssignRoleRequest,
    use_case: FromDishka[AssignRoleUseCase],
    token: str = Depends(get_current_token),
) -> MeResponse:
    try:
        return await use_case.execute(token, payload.user_id, payload.role)
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


