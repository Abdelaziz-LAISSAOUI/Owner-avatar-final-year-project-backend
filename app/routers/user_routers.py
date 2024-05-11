from fastapi import APIRouter, Depends,  HTTPException, status
from jose import JWTError, jwt
from typing import Annotated
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from ..database import get_db
import uuid
import os 

from ..crud.user_crud import get_user, create_user, get_user, get_user_by_email
from ..schemas.user_schemas import User, UserCreate

from ..schemas.token_schemas import TokenData
from .auth_routers import oauth2_scheme

from ..schemas.question_schemas import QuestionResponse, MCQResponse

from ..crud.question_crud import get_questions_not_in_history


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
        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id)
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
    return current_user


@user_router.get("/me/questions/", response_model=QuestionResponse)
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)], db: Session =Depends(get_db)
):
    
    # 1st: get user current lvl & get questions that match this lvl 
    questions = get_questions_not_in_history(db, current_user.current_lvl, current_user.id)

    # 2rd: question manipulation: 5 mcq, 5 iarrab, 2-3 writing that does not exists in the user History         

    # if not current_user.completed_test:
    #     # test logic
    #     return 

    return questions



"""
# @user_router.post("/me/questions/", response_model=list[Question], response_model=list[Feedback])
# async def read_own_items(
#     current_user: Annotated[User, Depends(get_current_active_user)], answers: Answers
# ):
    
#     # check responses   
#     # update user history
#     if not current_user.completed_test:
#         '''
#         test logic
#         '''        
#         # set user lvl
#         # (error rate < 80%  ? end assement : continue assement) 
#         # return feedback

#         return 

#     # analyze user history to decide whether he move to another lesson or practise more
#     # return feedback 



#     return current_user
"""