from dataclasses import dataclass
from domain.user.user_enums import Role

@dataclass
class RegisterUserRequestDTO:
    full_name: str
    email: str
    password: str
    phone_number: str
    role: Role

@dataclass
class RegisterUserResponseDTO:
    id: int
    email: str
    role: str
    status: str