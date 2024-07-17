from pydantic import BaseModel
import uuid

class ReportBase(BaseModel):
    user_id: uuid.UUID 
    question_id: uuid.UUID
    reason: str 

class ReportCreate(BaseModel):
    question_id: uuid.UUID
    reason: str 

class UserReport(BaseModel): 
    full_name: str 
    lesson_name : str
    reason: str

class ReportResponse(BaseModel):
    question_id: uuid.UUID
    body: str  
    lesson_name: str 
    users: list[UserReport]
    difficulty : str 
    type : str
    
    