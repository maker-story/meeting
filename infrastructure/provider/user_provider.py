
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from application.usecases.get_user_usecase import GetMeUseCase
from application.usecases.login_user_usercase import LoginUseCase
from application.usecases.logout_user_usecase import LogoutUseCase
from application.usecases.refresh_token_usecase import RefreshTokenUseCase
from infrastructure.database import get_db_session
from infrastructure.repository.postgres_refresh_token_repository import PostgresRefreshTokenRepository
from infrastructure.repository.postgres_user_repository import PostgresUserRepository
from infrastructure.security import BcryptPasswordHasher, JwtTokenService
from application.usecases.register_user_usecase import RegisterUserUseCase
from presentation.router.user_router import get_current_user_id_stub, get_login_use_case_stub, get_logout_use_case_stub, get_refresh_token_use_case_stub, get_register_use_case_stub, get_me_use_case_stub
from infrastructure.auth_gaurd import get_real_current_user_id  



def get_real_register_use_case(db: Session = Depends(get_db_session)):
    repository = PostgresUserRepository(db)
    hasher = BcryptPasswordHasher()
    return RegisterUserUseCase(repository, hasher)

def get_real_login_use_case(db: Session = Depends(get_db_session)):
    user_repo = PostgresUserRepository(db)
    refresh_token_repo = PostgresRefreshTokenRepository(db)
    password_hasher = BcryptPasswordHasher()
    token_service = JwtTokenService()
    return LoginUseCase(
        user_repository=user_repo,
        refresh_token_repository=refresh_token_repo,
        password_hasher=password_hasher,
        token_service=token_service
    )


def get_real_me_use_case(db: Session = Depends(get_db_session)):
    user_repo = PostgresUserRepository(db)
    return GetMeUseCase(user_repository=user_repo)


def get_real_refresh_token_use_case(db: Session = Depends(get_db_session)):
    refresh_token_repo = PostgresRefreshTokenRepository(db)
    user_repo = PostgresUserRepository(db)
    token_service = JwtTokenService()
    return RefreshTokenUseCase(refresh_token_repository=refresh_token_repo, user_repository=user_repo, token_service=token_service)


def get_real_logout_use_case(db: Session = Depends(get_db_session)):
    refresh_token_repo = PostgresRefreshTokenRepository(db)
    return LogoutUseCase(refresh_token_repository=refresh_token_repo)




def register_user_di(app: FastAPI):
    app.dependency_overrides[get_register_use_case_stub] = get_real_register_use_case
    app.dependency_overrides[get_login_use_case_stub] = get_real_login_use_case
    app.dependency_overrides[get_me_use_case_stub] = get_real_me_use_case
    app.dependency_overrides[get_refresh_token_use_case_stub] = get_real_refresh_token_use_case
    app.dependency_overrides[get_logout_use_case_stub] = get_real_logout_use_case
    app.dependency_overrides[get_refresh_token_use_case_stub] = get_real_refresh_token_use_case
    app.dependency_overrides[get_current_user_id_stub] = get_real_current_user_id
