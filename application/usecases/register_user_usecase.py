from dataclasses import dataclass

from domain.entity.user_entity import User
from domain.repository_interface.user_repository import IUserRepository
from domain.entity.user_entity import Role

class IPasswordHasher:
    def hash(self, password: str) -> str: pass


@dataclass
class RegisterUserRequestInput:
    full_name: str
    email: str
    password: str
    phone_number: str
    role: Role

@dataclass
class RegisterUserResponseOutput:
    id: int
    email: str
    role: str
    status: str



class RegisterUserUseCase:
    def __init__(self, user_repository: IUserRepository, password_hasher: IPasswordHasher):
        self.user_repository = user_repository
        self.password_hasher = password_hasher

    def execute(self, request: RegisterUserRequestInput) -> RegisterUserResponseOutput:
        # 1. Check if user exists
        existing_user = self.user_repository.find_by_email(request.email)
        if existing_user:
            raise ValueError("Email already in use")

        # 2. Hash password
        hashed_password = self.password_hasher.hash(request.password)

        # 3. Create Entity
        new_user = User(
            full_name=request.full_name,
            email=request.email,
            password_hash=hashed_password,
            phone_number=request.phone_number,
            role=request.role
        )

        # 4. Save to DB
        saved_user = self.user_repository.save(new_user)

        # 5. Return Output DTO
        return RegisterUserResponseOutput(
            id=saved_user.id,
            email=saved_user.email,
            role=saved_user.role.value,
            status=saved_user.status.value
        )