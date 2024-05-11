from ..schemas import question_schemas
from ..models import (Question, MCQ, Iaarab, Writing, History)
from sqlalchemy.orm import Session
import uuid


def create_question(db: Session, question: question_schemas.QuestionCreate):
    db_question = Question(**question.model_dump())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

def get_questions(db: Session):
    return db.query(Question).all()


def create_mcq(db: Session, question: question_schemas.MCQCreate):
    db_question = MCQ(**question.model_dump())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

def create_iraab(db: Session, question: question_schemas.Iraab):
    db_question = Iaarab(**question.model_dump())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

def create_writing(db: Session, question: question_schemas.Writing):
    db_question = Writing(**question.model_dump())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


def get_mcq_not_in_history(db: Session, current_lvl: str, user_id: uuid.UUID, limit:int =10 ):

    subquery = db.query(History.question_id).filter(History.user_id == user_id)
    
    questions = db.query(
        MCQ, Question
    ).filter(
        MCQ.id == Question.id
    ).filter(
        Question.lesson_name == current_lvl, ~Question.id.in_(subquery)
    ).limit(limit)
 
    res= []
    for q in questions:
        res.append({"mcq_data":q[0], "question_data":q[1]})
    return res
