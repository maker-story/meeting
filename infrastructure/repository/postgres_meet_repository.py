from sqlalchemy.orm import Session
from domain.entity.meet_entity import Meet
from domain.repository_interface.meet_repository_interface import IMeetRepository
from infrastructure.orm.meet_model import MeetModel
from infrastructure.orm.participant_model import MeetParticipantModel

class PostgresMeetRepository(IMeetRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save(self, meet: Meet) -> Meet:
        if meet.id:
            db_meet = self.db_session.query(MeetModel).filter(MeetModel.id == meet.id).first()
            db_meet.title = meet.title
            db_meet.is_active = meet.is_active
            db_meet.update_at = meet.update_at
            
            db_meet.participants.clear()
        else:
            db_meet = MeetModel(
                title=meet.title,
                meet_hash=meet.meet_hash,
                start_time=meet.start_time,
                expires_at=meet.expires_at,
                is_active=meet.is_active,
                creator_id=meet.creator_id,
                created_at=meet.created_at,
                update_at=meet.update_at
            )

        for participant_id in meet.participants_ids:
            participant_record = MeetParticipantModel(user_id=participant_id)
            db_meet.participants.append(participant_record)

        self.db_session.add(db_meet)
        self.db_session.commit()
        self.db_session.refresh(db_meet)

        meet.id = db_meet.id
        return meet

    def _map_to_domain(self, db_meet: MeetModel) -> Meet:
        if not db_meet:
            return None
            
        participant_ids = [p.user_id for p in db_meet.participants]

        return Meet(
            id=db_meet.id,
            title=db_meet.title,
            creator_id=db_meet.creator_id,
            start_time=db_meet.start_time,
            expires_at=db_meet.expires_at,
            meet_hash=db_meet.meet_hash,
            participants_ids=participant_ids,
            is_active=db_meet.is_active,
            created_at=db_meet.created_at,
            update_at=db_meet.update_at
        )

    def find_by_hash(self, meet_hash: str) -> Meet | None:
        db_meet = self.db_session.query(MeetModel).filter(MeetModel.meet_hash == meet_hash).first()
        return self._map_to_domain(db_meet)

    def find_by_id(self, meet_id: int) -> Meet | None:
        db_meet = self.db_session.query(MeetModel).filter(MeetModel.id == meet_id).first()
        return self._map_to_domain(db_meet)