from typing import List

from pydantic import BaseModel
from datetime import datetime


class CreateMeetRequestDTO(BaseModel):
    creator_id: int 
    title: str 
    start_time: datetime
    expires_at: datetime
    guest_usernames: List[str]

class CreateMeetResponseDTO(BaseModel):
    creator_id: int 
    title: str 
    start_time: datetime
    expires_at: datetime
    meet_hash: str
    id: int 
    message: str
