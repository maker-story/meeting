from sqlalchemy.orm import Session
from domain.entity.user_entity import User
from domain.repository_interface.user_repository_interface import IUserRepository
from infrastructure.orm.refresh_token import RefreshTokenModel
from infrastructure.orm.user_model import UserModel

class PostgresUserRepository(IUserRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save(self, user: User) -> User:
        db_user = UserModel(
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            email=user.email,
            password_hash=user.password_hash,
            role=user.role,
            is_active=user.is_active,
            created_at=user.created_at,
            update_at=user.update_at
        )
        self.db_session.add(db_user)
        self.db_session.commit()
        self.db_session.refresh(db_user)
        
        user.id = db_user.id # Map DB ID back to Entity
        return user

    def find_by_username(self, username: str) -> User | None:
        db_user = self.db_session.query(UserModel).filter(UserModel.username == username).first()
        if not db_user:
            return None
        return User(
            id=db_user.id,
            first_name=db_user.first_name,
            last_name=db_user.last_name,
            username=db_user.username,
            email=db_user.email,
            password_hash=db_user.password_hash,
            role=db_user.role,
            is_active=db_user.is_active,
            created_at=db_user.created_at,
            update_at=db_user.update_at
        )
    def find_by_id(self, user_id: int) -> User | None:
        db_user = self.db_session.query(UserModel).filter(UserModel.id == user_id).first()
        if not db_user:
            return None
        return User(
            id=db_user.id,
            first_name=db_user.first_name,
            last_name=db_user.last_name,
            username=db_user.username,
            email=db_user.email,
            password_hash=db_user.password_hash,
            role=db_user.role,
            is_active=db_user.is_active,
            created_at=db_user.created_at,
            update_at=db_user.update_at
        )
    
    def save_refresh_token(self, user_id: int, token: str) -> None:
        new_token = RefreshTokenModel(
            user_id=user_id,
            token=token
        )
        self.db_session.add(new_token)
        self.db_session.commit()

    def is_refresh_token_valid(self, user_id: int, token: str) -> bool:
        db_token = self.db_session.query(RefreshTokenModel).filter(
            RefreshTokenModel.user_id == user_id,
            RefreshTokenModel.token == token
        ).first()
        return db_token is not None

    def revoke_refresh_token(self, user_id: int, token: str) -> None:
        self.db_session.query(RefreshTokenModel).filter(
            RefreshTokenModel.user_id == user_id,
            RefreshTokenModel.token == token
        ).delete(synchronize_session=False)
        
        self.db_session.commit()