from fastapi import APIRouter, Depends, HTTPException

from presentation.dto.register_user_dto import RegisterRequestDTO, RegisterResponseDTO 
from presentation.presenter.register_user_presenter import UserPresenter
from application.usecases.register_user_usecase import RegisterUserRequestInput  
from application.usecases.register_user_usecase import RegisterUserUseCase

router = APIRouter(prefix="/users", tags=["Users"])

def get_register_use_case_stub() -> RegisterUserUseCase:
    raise NotImplementedError("This dependency must be overridden by the Composition Root.")

@router.post("/register", response_model=RegisterResponseDTO)
def register_user(
    request: RegisterRequestDTO,
    use_case: RegisterUserUseCase = Depends(get_register_use_case_stub)
):
    try:
        dto_request = RegisterUserRequestInput(
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