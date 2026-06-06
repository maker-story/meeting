from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from infrastructure.database import get_db_session
from infrastructure.user.user_postgres_repository import PostgresUserRepository
from infrastructure.user.security import BcryptPasswordHasher
from application.user.usecases.auth_usecase import RegisterUserUseCase
from presentation.user.user_router import get_register_use_case_stub

def get_real_register_use_case(db: Session = Depends(get_db_session)):
    repository = PostgresUserRepository(db)
    hasher = BcryptPasswordHasher()
    return RegisterUserUseCase(repository, hasher)

def register_user_di(app: FastAPI):
    app.dependency_overrides[get_register_use_case_stub] = get_real_register_use_case