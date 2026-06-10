
from fastapi import FastAPI
from fastapi.params import Depends
from sqlalchemy.orm import Session

from application.usecases.create_meet_usecase import CreateMeetUseCase
from infrastructure.database import get_db_session
from infrastructure.repository.postgres_meet_repository import PostgresMeetRepository
from infrastructure.repository.postgres_user_repository import PostgresUserRepository
from presentation.router.meet_router import create_meet_use_case_stub
from infrastructure.auth_gaurd import get_real_current_user_id
from presentation.router.meet_router import get_current_user_id_stub  


def create_real_meet_use_case(db: Session = Depends(get_db_session)):
    meet_repository = PostgresMeetRepository(db)
    user_repository =  PostgresUserRepository(db) # You would implement and use a UserRepository here
    return CreateMeetUseCase(meet_repository, user_repository)



def register_meet_di(app: FastAPI):
    app.dependency_overrides[create_meet_use_case_stub] = create_real_meet_use_case
    app.dependency_overrides[get_current_user_id_stub] = get_real_current_user_id