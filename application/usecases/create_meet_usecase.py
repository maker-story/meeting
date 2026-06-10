from abc import ABC, abstractmethod
from datetime import datetime
from typing import List
from pydantic.dataclasses import dataclass

from domain.entity.meet_entity import Meet
from domain.entity.user_entity import Role
from domain.repository_interface.meet_repository_interface import IMeetRepository
from domain.repository_interface.user_repository_interface import IUserRepository

@dataclass
class CreateMeetRequestInput:
        creator_id: int 
        title: str 
        start_time: datetime
        expires_at: datetime
        guest_usernames: List[str]
@dataclass
class CreateMeetResponseOutput:
        creator_id: int 
        title: str 
        start_time: datetime
        expires_at: datetime
        meet_hash: str
        id: int 


class INotificationService(ABC):
    @abstractmethod
    def send_meet_invitation(self, user_id: int, meet_hash: str, title: str) -> None:
        pass

class CreateMeetUseCase:
    def __init__(self, meet_repository: IMeetRepository, user_repository: IUserRepository, notification_service: INotificationService= ""):
        self.meet_repository = meet_repository
        self.user_repository = user_repository
        # self.notification_service = notification_service

    def execute(self, request: CreateMeetRequestInput) -> CreateMeetResponseOutput:
        creator = self.user_repository.find_by_id(request.creator_id)
        if not creator or creator.role not in [Role.Admin, Role.Host]:
            raise ValueError("Only Admins or Hosts can create a meet.")

        participant_ids = []
        for username in request.guest_usernames:
            if username == creator.username:
                 continue  # Skip adding the creator as a participant
            guest = self.user_repository.find_by_username(username)
            if guest:
                participant_ids.append(guest.id)
        if len(participant_ids) == 0:
            raise ValueError("At least one valid guest username must be provided.")

        new_meet = Meet(
            title=request.title,
            creator_id=request.creator_id,
            start_time=request.start_time,
            expires_at=request.expires_at,
            participants_ids=participant_ids
        )

        saved_meet = self.meet_repository.save(new_meet)

        # for p_id in participant_ids:
        #     self.notification_service.send_meet_invitation(p_id, saved_meet.meet_hash, saved_meet.title)


        return CreateMeetResponseOutput(
            creator_id=saved_meet.creator_id,
            title=saved_meet.title,
            start_time=saved_meet.start_time,
            expires_at=saved_meet.expires_at,
            meet_hash=saved_meet.meet_hash,
            id=saved_meet.id
        )