
from application.usecases.register_user_usecase import RegisterUserResponseOutput 
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