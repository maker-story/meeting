
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from infrastructure.database import get_db_session
from infrastructure.repository.user_reposiry import PostgresUserRepository
from infrastructure.security import BcryptPasswordHasher
from application.usecases.register_user_usecase import RegisterUserUseCase
from presentation.router.user_router import get_register_use_case_stub

def get_real_register_use_case(db: Session = Depends(get_db_session)):
    repository = PostgresUserRepository(db)
    hasher = BcryptPasswordHasher()
    return RegisterUserUseCase(repository, hasher)

def register_user_di(app: FastAPI):
    app.dependency_overrides[get_register_use_case_stub] = get_real_register_use_case