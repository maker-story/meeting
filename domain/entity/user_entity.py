from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from enum import Enum

class Role(str, Enum):
    Admin = "Admin"
    User = "User"


@dataclass
class User:
    first_name: str
    last_name: str
    email: str
    username: str
    password_hash: str
    role: Role
    is_active: bool = False
    id: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.now(datetime.timezone.utc))
    update_at: datetime = field(default_factory=datetime.now(datetime.timezone.utc))

    def activate(self):
        self.is_active = True 


