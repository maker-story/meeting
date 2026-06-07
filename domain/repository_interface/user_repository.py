
from abc import ABC, abstractmethod
from typing import Optional

from domain.entity.user_entity import User


class IUserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> User:
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        pass