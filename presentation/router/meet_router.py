from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.exceptions import HTTPException

from application.usecases.create_meet_usecase import CreateMeetRequestInput, CreateMeetUseCase
from presentation.dto.create_meet_dto import CreateMeetRequestDTO, CreateMeetResponseDTO
from presentation.presenter.meet_presenter import MeetPresenter



router = APIRouter(prefix="/meets", tags=["Meets"])

security_scheme = HTTPBearer()

def get_current_user_id_stub(credentials: HTTPAuthorizationCredentials = Depends(security_scheme)) -> int:
    raise NotImplementedError("This dependency must be overridden by the Composition Root.")

def create_meet_use_case_stub() -> CreateMeetUseCase:
    raise NotImplementedError("This dependency must be overridden by the Composition Root.")

@router.post("/meets", response_model=CreateMeetResponseDTO)
def create_meet(
    request: CreateMeetRequestDTO,
    current_user_id: int = Depends(get_current_user_id_stub),
    use_case: CreateMeetUseCase = Depends(create_meet_use_case_stub)
):
    try:
        dto_request = CreateMeetRequestInput(
            creator_id=current_user_id,
            title=request.title,
            start_time=request.start_time,
            expires_at=request.expires_at,
            guest_usernames=request.guest_usernames
        )
        
        dto_response = use_case.execute(dto_request)
        
        return MeetPresenter.format_create_response(dto_response)
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

##################################################################################################################