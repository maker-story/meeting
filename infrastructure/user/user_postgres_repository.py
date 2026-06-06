from sqlalchemy.orm import Session
from domain.user.user_entities import User
from domain.user.user_repositories import IUserRepository
from .user_orm_models import UserModel

class PostgresUserRepository(IUserRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save(self, user: User) -> User:
        db_user = UserModel(
            full_name=user.full_name,
            email=user.email,
            password_hash=user.password_hash,
            phone_number=user.phone_number,
            role=user.role,
            status=user.status,
            created_at=user.created_at
        )
        self.db_session.add(db_user)
        self.db_session.commit()
        self.db_session.refresh(db_user)
        
        user.id = db_user.id # Map DB ID back to Entity
        return user

    def find_by_email(self, email: str) -> User | None:
        db_user = self.db_session.query(UserModel).filter(UserModel.email == email).first()
        if not db_user:
            return None
        return User(
            id=db_user.id,
            full_name=db_user.full_name,
            email=db_user.email,
            password_hash=db_user.password_hash,
            phone_number=db_user.phone_number,
            role=db_user.role,
            status=db_user.status,
            created_at=db_user.created_at
        )