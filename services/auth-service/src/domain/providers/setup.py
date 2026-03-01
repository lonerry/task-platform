from dishka import Provider, Scope, provide, make_async_container

from infrastructure.postgres.database import PostgresDatabase
from infrastructure.postgres.repositories import UserRepository, RefreshTokenRepository
from domain.use_cases.register import RegisterUseCase
from domain.use_cases.login import LoginUseCase
from domain.use_cases.refresh import RefreshUseCase
from domain.use_cases.logout import LogoutUseCase
from domain.use_cases.me import MeUseCase
from domain.use_cases.assign_role import AssignRoleUseCase


class AppProvider(Provider):
    @provide(scope=Scope.APP)
    async def db(self) -> PostgresDatabase:
        return PostgresDatabase()

    @provide(scope=Scope.REQUEST)
    async def user_repo(self) -> UserRepository:
        return UserRepository()

    @provide(scope=Scope.REQUEST)
    async def refresh_repo(self) -> RefreshTokenRepository:
        return RefreshTokenRepository()

    @provide(scope=Scope.REQUEST)
    async def register_use_case(self, db: PostgresDatabase, user_repo: UserRepository) -> RegisterUseCase:
        return RegisterUseCase(db, user_repo)

    @provide(scope=Scope.REQUEST)
    async def login_use_case(self, db: PostgresDatabase, user_repo: UserRepository, refresh_repo: RefreshTokenRepository) -> LoginUseCase:
        return LoginUseCase(db, user_repo, refresh_repo)

    @provide(scope=Scope.REQUEST)
    async def refresh_use_case(self, db: PostgresDatabase, user_repo: UserRepository, refresh_repo: RefreshTokenRepository) -> RefreshUseCase:
        return RefreshUseCase(db, user_repo, refresh_repo)

    @provide(scope=Scope.REQUEST)
    async def logout_use_case(self, db: PostgresDatabase, refresh_repo: RefreshTokenRepository) -> LogoutUseCase:
        return LogoutUseCase(db, refresh_repo)

    @provide(scope=Scope.REQUEST)
    async def me_use_case(self, db: PostgresDatabase, user_repo: UserRepository) -> MeUseCase:
        return MeUseCase(db, user_repo)

    @provide(scope=Scope.REQUEST)
    async def assign_role_use_case(self, db: PostgresDatabase, user_repo: UserRepository) -> AssignRoleUseCase:
        return AssignRoleUseCase(db, user_repo)


container = make_async_container(AppProvider())
