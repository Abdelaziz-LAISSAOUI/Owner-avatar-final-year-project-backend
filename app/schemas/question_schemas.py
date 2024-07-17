import uuid
from pydantic import BaseModel

class QuestionBase(BaseModel): 
    body: str  
    lesson_name: str 
    difficulty : str
    type : str

class QuestionCreate(QuestionBase): 
    pass

class Question(QuestionBase): 
    id : uuid.UUID

class QuestionUpdate(Question):
    pass 

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

class MCQResponse(BaseModel):
    id : uuid.UUID 
    body: str
    lesson_name: str
    options: list[str]

class MCQUpdate(Question):
    option1: str 
    option2: str 
    option3: str 
    answer: str 

class MCQAnswer(BaseModel):
    id: uuid.UUID 
    user_answer: str

class MCQAnswerResponse(BaseModel):
    id: uuid.UUID 
    answer: str

################################################

class Iraab(BaseModel):
    answer: str
    segmentation : str 

class IraabCreate(Iraab):
    id: uuid.UUID

class IraabUpdate(Question):
    answer: str
    segmentation : str 

class IraabResponse(Question): 
    pass

class SegmentationResponse(BaseModel):
    segmentation : str

class IraabAnswer(BaseModel):
    id: uuid.UUID 
    user_answer: str

class IraabAnswerResponse(BaseModel):
    id: uuid.UUID 
    answer: str
################################################
class Writing(Question):
    pass

class WritingAnswer(BaseModel):
    id : uuid.UUID
    user_answer: str

class WritingAnswerResponse(BaseModel):
    id : uuid.UUID
    feedback: str
###############################################



class QuestionResponse(BaseModel):
    mcq: list[MCQResponse]
    iraab: list[IraabResponse]
    writing: Writing

class UserAnswers(BaseModel):
    mcq: list[MCQAnswer]
    iraab: list[IraabAnswer]
    writing: WritingAnswer

class AnswersRepsonse(BaseModel):
    mcq :list[MCQAnswerResponse]
    iraab:list[IraabAnswerResponse]
    writing: WritingAnswerResponse

    