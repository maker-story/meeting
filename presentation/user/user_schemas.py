from pydantic import BaseModel, EmailStr
from domain.user.user_enums import Role

class RegisterRequestSchema(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    phone_number: str
    role: Role

class RegisterResponseSchema(BaseModel):
    id: int
    email: str
    role: str
    status: str
    message: str