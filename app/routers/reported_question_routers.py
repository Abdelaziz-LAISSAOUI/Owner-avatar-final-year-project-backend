from fastapi import APIRouter, Depends 
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user_schemas import User
from ..schemas import reported_question_schemas
from ..crud import reported_question_crud
from ..routers.user_routers import get_current_user
from ..routers.teacher_routers import is_teacher


reported_question_router = APIRouter(
    prefix="/v1/reported_questions",
    tags=["reported_questions"],
)


@reported_question_router.post("/",  status_code=201, responses={401: {"description": "Unauthorized"}})
def create_reported_question(reported_question: reported_question_schemas.ReportCreate, user:User =  Depends(get_current_user),  db: Session = Depends(get_db)):
    new_reported_question= reported_question_schemas.ReportBase(**reported_question.model_dump() , user_id=user.id)
    return reported_question_crud.create_reported_question(db, new_reported_question)

# only teachers 
@reported_question_router.get("/", response_model=list[reported_question_schemas.ReportResponse], responses={401: {"description": "Unauthorized"}})
def get_reported_questions(skip:int = 0, limit:int = 10, teacher = Depends(is_teacher), db: Session = Depends(get_db)):
    return reported_question_crud.get_repoted_question_with_users(db, limit, skip)
