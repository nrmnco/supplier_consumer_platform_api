from sqlmodel import Session, select
from src.models.cities import Cities
from typing import List

def get_all_cities(session: Session) -> List[Cities] | None:
    return session.exec(select(Cities)).all()
