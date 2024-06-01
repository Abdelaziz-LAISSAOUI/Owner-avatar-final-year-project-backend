from sqlalchemy.orm import Session
from ..models import History 
from ..schemas.history_schemas import HistoryCreate
import uuid
def create_history(db: Session, history: HistoryCreate):
    db_history = History(**history.model_dump())
    db.add(db_history)
    db.commit()
    db.refresh(db_history)
    return db_history


def get_user_history(db: Session, user_id: uuid.UUID, lesson_name: str):
    return db.query(History).filter(History.user_id == user_id, History.lesson_name == lesson_name).all()