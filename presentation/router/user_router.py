from fastapi import APIRouter, Depends, HTTPException
from starlette import status


from application.usecases.login_user_usercase import LoginRequestInput, LoginUseCase
from presentation.dto.login_user_dto import LoginRequestDTO, LoginResponseDTO
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
            first_name=request.first_name,
            last_name=request.last_name,
            username=request.username,
            email=request.email,
            password=request.password,
            role=request.role
        )
        
        dto_response = use_case.execute(dto_request)
        
        return UserPresenter.format_register_response(dto_response)
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

##################################################################################################################

def get_login_use_case_stub() -> RegisterUserUseCase:
    raise NotImplementedError("This dependency must be overridden by the Composition Root.")


@router.post("/login", response_model=LoginResponseDTO)
def login_user(
    request: LoginRequestDTO,
    use_case: LoginUseCase = Depends(get_login_use_case_stub)
):
    try:
        dto_request = LoginRequestInput(
            username=request.username,
            password=request.password
        )
        dto_response = use_case.execute(dto_request)
        return dto_response

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )

