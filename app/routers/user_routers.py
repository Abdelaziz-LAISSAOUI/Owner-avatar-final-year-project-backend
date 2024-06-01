from fastapi import APIRouter, Depends,  HTTPException, status
from jose import JWTError, jwt
from typing import Annotated
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from ..database import get_db
import uuid
import os 

from ..crud.user_crud import get_user, create_user, get_user, get_user_by_email, end_initial_assement, move_to_next_lesson
from ..schemas.user_schemas import User, UserCreate

from ..schemas.token_schemas import TokenData
from .auth_routers import oauth2_scheme

from ..schemas.question_schemas import QuestionResponse, SegmentationResponse, UserAnswers, AnswersRepsonse

from ..crud.question_crud import get_questions_not_in_history, get_segmentation, get_iraab_answers, get_mcq_answers

from ..schemas.history_schemas import HistoryCreate

from ..crud.history_crud import create_history, get_user_history

user_router = APIRouter(
    prefix="/v1/users",
    tags=["users"],
)

load_dotenv()


SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("sub")
        role: str = payload.get("role")
        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id, role=role)
    except JWTError:
        raise credentials_exception
    user_id = uuid.UUID(token_data.id)
    user = get_user(db, user_id=user_id)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user



@user_router.post("/", response_model=User, status_code=201, responses={409: {"description": "Conflict"}})
async def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    user_exist = get_user_by_email(db, user.email)
    if user_exist: 
        raise HTTPException(status_code=409, detail="User already exists")
    new_user = create_user(db, user)
    return new_user

@user_router.get("/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user # statistics 


@user_router.get("/me/questions/", response_model=QuestionResponse)
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)], db: Session =Depends(get_db)
):    
    return  get_questions_not_in_history(db, current_user.current_lvl, current_user.id)




@user_router.get("/me/questions/segmentation/{question_id}", response_model=SegmentationResponse)
async def get_segmentation_from_id(current_user: Annotated[User, Depends(get_current_active_user)], question_id: str, db: Session = Depends(get_db)):     
    segmentation = get_segmentation(db, uuid.UUID(question_id))
    if not segmentation: 
        raise HTTPException(404,  detail="question does not exists")
    return segmentation



@user_router.post("/me/questions/", response_model=AnswersRepsonse)
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)], answers: UserAnswers, db: Session = Depends(get_db)
):
    
    # check responses   
    mcq_responses = get_mcq_answers(db, answers.mcq)
    iraab_responses = get_iraab_answers(db, answers.iraab)
    print("mcq_responses", mcq_responses)
    print("iraab_response", iraab_responses)

    # writing_feedback = get_feedback(answers.writing.user_response)

    # update user history
    for response in mcq_responses:         
        for a in answers.mcq:
            if response.id == a.id : 
                user_answer = a.user_answer
        
        feedback = user_answer==response.answer
        new_history = HistoryCreate(user_id = current_user.id,  question_id = response.id,  user_answer = user_answer,  feedback = str(feedback), lesson_name=current_user.current_lvl, type='mcq')
        _= create_history(db, new_history)

    for response in iraab_responses: 
        for a in answers.iraab: 
            if response.id == a.id : 
                user_answer = a.user_answer

        feedback = user_answer==response.answer
        new_history = HistoryCreate(user_id = current_user.id,  question_id = response.id,  user_answer = user_answer,  feedback = str(feedback), lesson_name=current_user.current_lvl, type='iraab')
        _= create_history(db, new_history)

    # # new_history = HistoryCreate( user_id = current_user.id,  question_id = answers.writing.id,  user_answer = answers.writing.user_response,  feedback = writing_feedback)
    # # _= create_history(db, new_history)

    user_history = get_user_history(db, current_user.id, current_user.current_lvl)


    correct_answers= 0
    total_question = 0
    for h in user_history:
        if h.type == 'mcq' or h.type =='iraab': 
            total_question+=1
            if h.feedback == 'True': 
                correct_answers +=1

    if not current_user.completed_test:
        '''test logic'''        
        if total_question>= 10:  
            if total_question * 0.9 > correct_answers: 
                end_initial_assement(db, current_user.id)
            else:
                _= move_to_next_lesson(db, current_user.id)
        
        return {"mcq":mcq_responses, "iraab": iraab_responses } # add writing feedback 


    # analyze user history to decide whether he move to another lesson or practise more    
    if total_question >= 20 and total_question <30:    
        if total_question == correct_answers: 
            _=move_to_next_lesson(db, current_user.id)

    if total_question >= 30 and total_question <40:
        if total_question* 0.9 <= correct_answers :
            _=move_to_next_lesson(db, current_user.id)

    if total_question >= 40 and total_question <50:
        if total_question* 0.8 <= correct_answers : 
            _=move_to_next_lesson(db, current_user.id)

    if total_question * 0.7 <= correct_answers: 
        _=move_to_next_lesson(db, current_user.id)
    

    return {"mcq":mcq_responses, "iraab": iraab_responses } # add writing feedback 
