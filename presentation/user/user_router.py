from fastapi import APIRouter, Depends, HTTPException
from presentation.user.user_schemas import RegisterRequestSchema, RegisterResponseSchema
from presentation.user.user_presenters import UserPresenter
from application.user.dtos import RegisterUserRequestDTO
from application.user.usecases.auth_usecase import RegisterUserUseCase

router = APIRouter(prefix="/users", tags=["Users"])

def get_register_use_case_stub() -> RegisterUserUseCase:
    raise NotImplementedError("This dependency must be overridden by the Composition Root.")

@router.post("/register", response_model=RegisterResponseSchema)
def register_user(
    request: RegisterRequestSchema,
    use_case: RegisterUserUseCase = Depends(get_register_use_case_stub)
):
    try:
        dto_request = RegisterUserRequestDTO(
            full_name=request.full_name,
            email=request.email,
            password=request.password,
            phone_number=request.phone_number,
            role=request.role
        )
        
        dto_response = use_case.execute(dto_request)
        
        return UserPresenter.format_register_response(dto_response)
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))