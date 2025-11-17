from datetime import datetime
from sqlmodel import Session, select
from src.models.linkings import Linkings, LinkingStatus
from src.schemas.linkings import LinkingSchema

def create_linking(session: Session, data: LinkingSchema, consumer_company_id: int, requested_user_id, company_id: int) -> Linkings:
    linking_data = data

    # Create linking instance
    linking = Linkings(**linking_data.model_dump(), supplier_company_id=company_id, consumer_company_id=consumer_company_id, requested_by_user_id=requested_user_id, status=LinkingStatus.pending)
    session.add(linking)
    session.flush()

    session.commit()
    session.refresh(linking)

    return linking

def get_linkings_by_company(session: Session, company_id: int):
    statement = select(Linkings).where(
        (Linkings.supplier_company_id == company_id) | (Linkings.consumer_company_id == company_id)
    )
    results = session.exec(statement).all()
    return results

def check_if_exists(session: Session, consumer_company_id: int, supplier_company_id: int):
    linking = session.exec(select(Linkings).where(
        (Linkings.consumer_company_id == consumer_company_id) & (Linkings.supplier_company_id == supplier_company_id)
        )).first()
    
    if not linking:
        return False
    
    return True

def check_if_linked(session: Session, consumer_company_id: int, supplier_company_id: int):
    linking = session.exec(select(Linkings).where(
        (Linkings.consumer_company_id == consumer_company_id) & (Linkings.supplier_company_id == supplier_company_id) & (Linkings.status == LinkingStatus.accepted)
        )).first()
    
    if not linking:
        return False
    
    return True


def get_linking(session: Session, consumer_company_id: int, supplier_company_id: int):
    linking = session.exec(select(Linkings).where(
        (Linkings.consumer_company_id == consumer_company_id) & (Linkings.supplier_company_id == supplier_company_id) & (Linkings.status == LinkingStatus.accepted)
        )).first()
    
    if not linking:
        raise ValueError(f"Linking not found")
    
    return linking


def update_due_response(session: Session, linking_id: int, responded_user_id: int, status: str):
    linking = session.get(Linkings, linking_id)

    if not linking:
        raise ValueError("Linking not found")
    
    setattr(linking, 'status', status)
    setattr(linking, 'responded_by_user_id', responded_user_id)
    setattr(linking, 'assigned_salesman_user_id', responded_user_id)
    setattr(linking, 'updated_at', datetime.now())

    session.commit()
    session.refresh(linking)
    
    return linking