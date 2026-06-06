from application.user.dtos import RegisterUserResponseDTO
from .user_schemas import RegisterResponseSchema

class UserPresenter:
    @staticmethod
    def format_register_response(dto: RegisterUserResponseDTO) -> RegisterResponseSchema:
        return RegisterResponseSchema(
            id=dto.id,
            email=dto.email,
            role=dto.role,
            status=dto.status,
            message="User registered successfully."
        )