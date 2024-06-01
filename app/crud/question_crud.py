from ..schemas import question_schemas
from ..models import (Question, MCQ, Iraab, Writing, History)
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

def create_iraab(db: Session, question: question_schemas.IraabCreate):
    db_question = Iraab(**question.model_dump())
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


def get_questions_not_in_history(db: Session, current_lvl: str, user_id: uuid.UUID, limit:int =3 ):

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


    iraab_questions = db.query(
        Question
    ).filter(
        Question.lesson_name == current_lvl, Question.type == "iraab" , ~Question.id.in_(subquery)
    ).limit(limit).all()


    writing_question = db.query(
        Question
    ).filter(
        Question.lesson_name == current_lvl, Question.type == "writing", ~Question.id.in_(subquery)
    ).first()
    

    print("iraab", iraab_questions)
    print("writing", writing_question)

    return {"mcq":res, "iraab": iraab_questions, "writing": writing_question}



def edit_question(db: Session, question_id: str, question: question_schemas.Question):

    db_question = get_question(db, uuid.UUID(question_id))

    if not db_question:
        return None
    
    if  db_question.type == 'mcq':
        print("MCQ ", question_id)
        db_question = db.query(Question, MCQ).filter(Question.id == MCQ.id).filter(Question.id == db_question.id).first()
    elif question.type == 'iraab':
        db_question = db.query(Question, Iraab).filter(Question.id == Iraab.id).filter(Question.id == db_question.id).first()
        print("IRABAB ", question_id)
    


    print(db_question[0])
    print(db_question[1])


    return db_question
    # for k, v in question: 
    #     setattr(db_question, k, v)
    # db.commit()
    # db.refresh(db_question)
    # return db_question




def edit_question_mcq(db: Session, question_id: uuid.UUID, question: question_schemas.MCQUpdate):
    db_q  = db.query(Question, MCQ).filter(Question.id == MCQ.id).filter(Question.id == question_id).first()
    db_question = get_question(db, question_id)
    db_mcq = db.query(MCQ).filter(MCQ.id == question_id).first()


    if not db_q:
        return None
    

    updated_question = Question(
        id=question.id ,body=question.body ,lesson_name=question.lesson_name ,difficulty=question.difficulty ,type=question.type
    )

    updated_mcq = MCQ(id=question.id , answer=question.answer , option1= question.option1, option2= question.option2, option3=question.option3 )

    db_question.body = updated_question.body
    db_question.lesson_name = updated_question.lesson_name
    db_question.difficulty = updated_question.difficulty
    db_question.type = updated_question.type


    db_mcq.answer = updated_mcq.answer
    db_mcq.option1 = updated_mcq.option1
    db_mcq.option2 = updated_mcq.option2
    db_mcq.option3 = updated_mcq.option3


    db.commit()
    db.refresh(db_question)
    return db_question


def edit_question_iraab(db: Session, question_id: uuid.UUID, question: question_schemas.IraabUpdate):
    db_q = db.query(Question, Iraab).filter(Question.id == Iraab.id).filter(Question.id == question_id).first()

    if not db_q:
        return None
    

    updated_question = Question(
        id=question.id ,body=question.body ,lesson_name=question.lesson_name ,difficulty=question.difficulty ,type=question.type
    )
    updated_iraab = Iraab(
        id=question.id ,  answer=question.answer ,  segmentation=question.segmentation     
    )    

    db_question = db_q[0]
    db_question.body = updated_question.body
    db_question.lesson_name = updated_question.lesson_name
    db_question.difficulty = updated_question.difficulty
    db_question.type = updated_question.type


    db_iraab = db_q[1]
    db_iraab.answer = updated_iraab.answer
    db_iraab.segmentation = updated_iraab.segmentation

    db.commit()
    db.refresh(db_question)
    return db_question


def edit_question_writing(db: Session, question_id: uuid.UUID, question: question_schemas.Question):
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

def get_segmentation(db: Session, question_id: uuid.UUID): 
    return db.query(Iraab.segmentation).filter(Iraab.id == question_id).first()
    

def get_mcq_answers(db: Session, mcq_answers: list[question_schemas.MCQAnswer]):
    db_questions = [db.query(MCQ.id , MCQ.answer).filter(MCQ.id == q.id).first() for q in mcq_answers] 
    return db_questions 

def get_iraab_answers(db: Session, iraab_answers: list[question_schemas.IraabAnswer]):
    db_questions = [db.query(Iraab.id , Iraab.answer).filter(Iraab.id == q.id).first() for q in iraab_answers] 
    return db_questions 

# TODO: get writing feedback
