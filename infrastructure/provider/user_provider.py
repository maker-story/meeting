
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from application.usecases.login_user_usercase import LoginUseCase
from infrastructure.database import get_db_session
from infrastructure.repository.user_reposiry import PostgresUserRepository
from infrastructure.security import BcryptPasswordHasher, JwtTokenService
from application.usecases.register_user_usecase import RegisterUserUseCase
from presentation.router.user_router import get_login_use_case_stub, get_register_use_case_stub



def get_real_register_use_case(db: Session = Depends(get_db_session)):
    repository = PostgresUserRepository(db)
    hasher = BcryptPasswordHasher()
    return RegisterUserUseCase(repository, hasher)

def get_real_login_use_case():
    db_session = next(get_db_session())
    user_repo = PostgresUserRepository(db_session)
    password_hasher = BcryptPasswordHasher()
    token_service = JwtTokenService()
    return LoginUseCase(
        user_repository=user_repo,
        password_hasher=password_hasher,
        token_service=token_service
    )


def register_user_di(app: FastAPI):
    app.dependency_overrides[get_register_use_case_stub] = get_real_register_use_case
    app.dependency_overrides[get_login_use_case_stub] = get_real_login_use_case
