
from application.usecases.login_user_usercase import LoginResponseOutput
from application.usecases.register_user_usecase import RegisterUserResponseOutput 
from presentation.dto.login_user_dto import LoginResponseDTO
from presentation.dto.register_user_dto import RegisterResponseDTO 

class UserPresenter:
    @staticmethod
    def format_register_response(dto: RegisterUserResponseOutput) -> RegisterResponseDTO:
        return RegisterResponseDTO(
            id=dto.id,
            email=dto.email,
            username=dto.username,
            role=dto.role,
            is_active=dto.is_active,
            message="User registered successfully."
        )
    
    @staticmethod
    def format_login_response(dto: LoginResponseOutput) -> LoginResponseDTO:
        return LoginResponseDTO (
            access_token=dto.access_token,
            refresh_token=dto.refresh_token,
            token_type="bearer",
            message="Login successful."
        )
    
