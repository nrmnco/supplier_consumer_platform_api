from sqlmodel import Session, select
from src.models.linkings import Linkings, LinkingStatus
from src.schemas.linkings import LinkingSchema

def create_linking(session: Session, data: LinkingSchema, consumer_company_id: int, requested_user_id, company_id: int) -> Linkings:
    linking_data = data

    # Create linking instance
    linking = Linkings(**linking_data.model_dump(), company_id=company_id, consumer_company_id=consumer_company_id, requested_by_user_id=requested_user_id, status=LinkingStatus.pending)
    session.add(linking)
    session.flush()

    session.commit()
    session.refresh(linking)

    return linking