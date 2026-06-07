
from pydantic import BaseModel, EmailStr
from domain.entity.user_entity import Role

class RegisterRequestDTO(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    phone_number: str
    role: Role

class RegisterResponseDTO(BaseModel):
    id: int
    email: str
    role: str
    status: str
    message: str