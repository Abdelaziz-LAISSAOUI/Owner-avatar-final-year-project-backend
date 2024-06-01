import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from ..schemas import question_schemas
from ..crud import question_crud
from ..routers.teacher_routers import is_teacher

question_router = APIRouter(
    prefix="/v1/questions",
    tags=["questions"],
)


@question_router.delete("/{question_id}/", response_model=question_schemas.Question, responses={401: {"description": "Unauthorized"}, 409: {"description": "Conflict"}})
def delete_question(question_id: uuid.UUID ,  db: Session = Depends(get_db)): # TODO: add teacher middlweare
    question = question_crud.delete_question(db, question_id=question_id)
    if not question:
        raise HTTPException(status_code=409, detail="Question does not exists")
    return question        

@question_router.put("/mcq/{question_id}/",  responses={403: {"description": "Forbidden"}, 409: {"description": "Conflict"}})
def update_question(question_id: str, updated_question: question_schemas.MCQUpdate, teacher = Depends(is_teacher),   db: Session = Depends(get_db)):   
    question = question_crud.edit_question_mcq(db, uuid.UUID(question_id), updated_question)
    if not question:
        raise HTTPException(status_code=409, detail="Question does not exists")
    return question

@question_router.put("/iraab/{question_id}/", response_model=question_schemas.Question , responses={403: {"description": "Forbidden"}, 409: {"description": "Conflict"}})
def update_question(question_id: str, updated_question: question_schemas.IraabUpdate, teacher = Depends(is_teacher),   db: Session = Depends(get_db)): 
    question = question_crud.edit_question_iraab(db, uuid.UUID(question_id), updated_question)
    if not question:
        raise HTTPException(status_code=409, detail="Question does not exists")
    return question


# @question_router.patch("/writing/{question_id}/",  responses={401: {"description": "Unauthorized"}, 409: {"description": "Conflict"}})
# def update_question(question_id: str, updated_question: question_schemas.QuestionUpdate,   db: Session = Depends(get_db)): # TODO: add teacher middlweare
#     question = question_crud.edit_question(db, question_id, updated_question)
#     if not question:
#         raise HTTPException(status_code=409, detail="Question does not exists")
#     return question