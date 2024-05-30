from ..schemas import question_schemas
from ..models import (Question, MCQ, Iaarab, Writing, History)
from sqlalchemy.orm import Session
import random
import uuid


def create_question(db: Session, question: question_schemas.QuestionCreate):
    db_question = Question(**question.model_dump())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

def get_questions(db: Session):
    return db.query(Question).all()


def get_question(db: Session, question_id: uuid.UUID):
    return db.query(Question).filter(Question.id == question_id).first()


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


def get_questions_not_in_history(db: Session, current_lvl: str, user_id: uuid.UUID, limit:int =10 ):

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
        # place answer randomly in options 
        options=['', '', '', '']
        options[random.randrange(4)]= q[0].answer
        restOptions=[q[0].option1, q[0].option2, q[0].option3]
        temp=0

        for i in range(len(options)):
            if options[i] == '':
                options[i] = restOptions[temp]
                temp +=1 

        # res.append({"mcq_data":q[0], "question_data":q[1]})
        res.append({
            "id":q[0].id, 
            "options":options,
            "body":q[1].body, 
            "lesson_name":q[1].lesson_name,
        })

    return {"mcq":res}

def edit_question(db: Session, question_id: uuid.UUID, question: Question):
    db_question = get_question(db, question_id)
    if not db_question:
        return None
    for k, v in question: 
        setattr(db_question, k, v)
    db.commit()
    db.refresh(db_question)
    return db_question

def delete_question(db: Session, question_id: uuid.UUID):
    db_question = get_question(db, question_id)
    if not db_question:
        return None
    db.delete(db_question)
    db.commit()
    return db_question