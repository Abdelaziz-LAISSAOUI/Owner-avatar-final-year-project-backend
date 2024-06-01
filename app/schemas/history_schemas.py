import uuid
from pydantic import BaseModel
from datetime import datetime


class HistoryBase(BaseModel): # add difficulty
    user_id: uuid.UUID
    question_id: uuid.UUID
    user_answer: str
    feedback: str
    lesson_name : str
    type : str

class HistoryCreate(HistoryBase):
    pass

class History(HistoryBase):
    date: datetime