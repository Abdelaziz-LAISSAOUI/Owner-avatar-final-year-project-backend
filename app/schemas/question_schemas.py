import uuid
from pydantic import BaseModel

class QuestionBase(BaseModel): 
    body: str  
    lesson_name: str 

class QuestionCreate(QuestionBase): 
    pass

class Question(QuestionBase): 
    id : uuid.UUID 

################################################
class MCQBase(BaseModel):
    option1: str 
    option2: str 
    option3: str 
    answer: str 

class MCQ(MCQBase):
    id : uuid.UUID

class MCQCreate(MCQ):
    pass
################################################

class Iraab(Question):
    asnwer: str
################################################
class Writing(Question):
    pass

################################################
class CombinedResponse(BaseModel):
    mcq_data: MCQCreate
    question_data: Question