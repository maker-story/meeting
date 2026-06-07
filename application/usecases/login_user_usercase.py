from abc import ABC, abstractmethod
from dataclasses import dataclass
from pydantic import EmailStr

from .register_user_usecase import IPasswordHasher
from domain.repository_interface.user_repository import IUserRepository 


class ITokenService(ABC):
    @abstractmethod
    def generate_access_token(self, data: dict) -> str:
        pass

@dataclass
class LoginRequestInput:
    username: str 
    password: str

@dataclass
class LoginResponseOutput:
    access_token: str
    token_type: str = "bearer"


class LoginUseCase:
    def __init__(
        self, 
        user_repository: IUserRepository, 
        password_hasher: IPasswordHasher,
        token_service: ITokenService
    ):
        self.user_repository = user_repository
        self.password_hasher = password_hasher
        self.token_service = token_service

    def execute(self, request: LoginRequestInput) -> LoginResponseOutput:
        user = self.user_repository.find_by_username(request.username)
        if not user:
            raise ValueError("Username not found.") 

        if not self.password_hasher.verify_password(request.password, user.password_hash):
            raise ValueError("Password is not valid.")

        token_data = {"sub": str(user.id), "username": user.username, "role": user.role.value }
        access_token = self.token_service.generate_access_token(token_data)

        return LoginResponseOutput(access_token=access_token)