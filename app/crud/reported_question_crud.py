from sqlalchemy.orm import Session 
from ..schemas.reported_question_schemas import ReportBase, ReportResponse, UserReport
from ..models import ReportedQuestion, Question, User


def create_reported_question(db: Session, question: ReportBase):
    db_question = ReportedQuestion(**question.model_dump())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return "success"


def get_repoted_question_with_users(db: Session, limit:int = 10, skip: int = 0):
    reports = db.query(
        Question, User, ReportedQuestion.reason 
    ).filter(
        ReportedQuestion.question_id == Question.id , ReportedQuestion.user_id == User.id  
    ).group_by(ReportedQuestion.question_id, Question.id, User.id).offset(skip).limit(limit).all()


    questions = set([q[0] for q in reports])
    response  = [ ReportResponse(question_id= q.id, body= q.body, lesson_name= q.lesson_name, users= [], type=q.type, difficulty= q.difficulty) for q in questions ]
    
    for r in reports: 
        for res in response: 
            if str(r[0].id) == str(res.question_id): 
                user = UserReport(full_name=r[1].full_name, lesson_name=r[1].current_lvl, reason=r[2])
                res.users.append(user)

    return response