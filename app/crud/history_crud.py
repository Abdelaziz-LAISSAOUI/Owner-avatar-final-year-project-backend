from sqlalchemy.orm import Session
from ..models import History 
from ..schemas.history_schemas import HistoryCreate

def create_history(db: Session, history: HistoryCreate):
    db_history = History(**history.model_dump())
    db.add(db_history)
    db.commit()
    db.refresh(db_history)
    return db_history