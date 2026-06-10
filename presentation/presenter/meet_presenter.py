from application.usecases.create_meet_usecase import CreateMeetResponseOutput
from presentation.dto.create_meet_dto import CreateMeetResponseDTO

class MeetPresenter:
    @staticmethod
    def format_create_response(dto: CreateMeetResponseOutput) -> CreateMeetResponseDTO:
        return CreateMeetResponseDTO(
            creator_id=dto.creator_id,
            title=dto.title,
            start_time=dto.start_time,
            expires_at=dto.expires_at,
            meet_hash=dto.meet_hash,
            id=dto.id,
            message="Meeting created successfully."
        )