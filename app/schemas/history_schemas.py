import uuid
from pydantic import BaseModel
from datetime import datetime


class HistoryBase(BaseModel):
    user_id: uuid.UUID
    question_id: uuid.UUID
    user_answer: str
    feedback: str

class HistoryCreate(HistoryBase):
    pass

class History(HistoryBase):
    date: datetime