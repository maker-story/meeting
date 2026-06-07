from sqlalchemy import Column, Integer, String, Enum, DateTime
from datetime import datetime

from domain.entity.user_entity  import Role, UserStatus
from ..database import Base


class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    role = Column(Enum(Role), nullable=False)
    status = Column(Enum(UserStatus), default=UserStatus.Pending)
    created_at = Column(DateTime, default=datetime.utcnow)