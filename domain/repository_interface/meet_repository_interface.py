from abc import ABC, abstractmethod
from typing import Optional

from domain.entity.meet_entity import Meet


class IMeetRepository(ABC):
    @abstractmethod
    def save(self, meet: Meet) -> Meet:
        pass

    @abstractmethod
    def find_by_hash(self, meet_hash: str) -> Optional[Meet]:
        pass

    @abstractmethod
    def find_by_id(self, meet_id: int) -> Optional[Meet]:
        pass