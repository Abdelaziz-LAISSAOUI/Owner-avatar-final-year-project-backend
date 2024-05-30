from datetime import timedelta 
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from dotenv import load_dotenv
from ..crud.user_crud import authenticate_user
from ..crud.teacher_crud import authenticate_teacher
from ..crud.admin_crud import authenticate_admin
from ..schemas.teacher_schemas import TeacherCreate
from ..schemas.admin_schemas import AdminCreate
from ..utilities import  create_access_token
from ..database import get_db
from ..schemas.token_schemas import Token
import os

load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES =os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES')


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

auth_router = APIRouter(tags=["authentification"])

@auth_router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)
) -> Token:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"sub": str(user.id), "role": "user"}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@auth_router.post("/v1/teachers/token", response_model=Token)
def login_in_teacher(teacher: TeacherCreate, db: Session = Depends(get_db)):
    teacher = authenticate_teacher(db, teacher.username, teacher.password)
    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"sub": teacher.username, "role": "teacher"}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@auth_router.post("/v1/admins/token", response_model=Token)
def login_in_admin(admin: AdminCreate, db: Session = Depends(get_db)):
    admin = authenticate_admin(db, admin.username, admin.password)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"sub": admin.username, "role": "admin"}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
