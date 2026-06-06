from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from .user_enums import Role, UserStatus

@dataclass
class User:
    full_name: str
    email: str
    password_hash: str
    phone_number: str
    role: Role
    id: Optional[int] = None
    status: UserStatus = UserStatus.Pending
    created_at: datetime = field(default_factory=datetime.utcnow)

    def activate(self):
        self.status = UserStatus.Active