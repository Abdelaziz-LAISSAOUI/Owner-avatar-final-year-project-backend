from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Request, status
from jose import jwt
from sqlalchemy.orm import Session
from app.database import get_db
from ..schemas import teacher_schemas
from ..crud import teacher_crud
from ..routers.admin_routers import is_admin
import os 

teacher_router = APIRouter(
    prefix="/v1/teachers",
    tags=["teachers"],
)


load_dotenv()


SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')



async def is_teacher(req: Request, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You are not allowed to perform this action",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        token = req.headers["Authorization"].split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("sub")
        role: str = payload.get("role")
        if id is None:
            raise credentials_exception    
    except:
        raise credentials_exception
    
    teacher = teacher_crud.get_teacher(db, id)
    if teacher is None:
        raise credentials_exception
    return teacher


@teacher_router.post("/", response_model=teacher_schemas.TeacherResponse, status_code=201, responses={401: {"description": "Unauthorized"}})
def create_teacher(teacher: teacher_schemas.TeacherCreate, admin = Depends(is_admin),  db: Session = Depends(get_db)):
    exist_teacher = teacher_crud.get_teacher(db, teacher.username)
    if exist_teacher:
        raise HTTPException(status_code=409, detail="Teacher already exists")

    return teacher_crud.create_teacher(db, teacher)

@teacher_router.get("/", response_model=list[teacher_schemas.TeacherResponse], responses={401: {"description": "Unauthorized"}})
def get_teachers(skip:int = 0, limit:int = 100, admin = Depends(is_admin),  db: Session = Depends(get_db)):
    return teacher_crud.get_teachers(db, skip, limit)


@teacher_router.delete("/{teacher_username}/", response_model=teacher_schemas.TeacherResponse, responses={401: {"description": "Unauthorized"}, 409: {"description": "Conflict"}})
def delete_teacher(teacher_username: str , admin = Depends(is_admin),  db: Session = Depends(get_db)):
    teacher = teacher_crud.delete_teacher(db, teacher_username=teacher_username)
    if not teacher:
        raise HTTPException(status_code=409, detail="Teacher does not exists")
    return teacher        

@teacher_router.patch("/{teacher_username}/", response_model=teacher_schemas.TeacherResponse, responses={401: {"description": "Unauthorized"}, 409: {"description": "Conflict"}})
def update_teacher(teacher_username: str, updated_teacher: teacher_schemas.TeacherUpdate, admin = Depends(is_admin),  db: Session = Depends(get_db)):
    teacher = teacher_crud.update_teacher(db, teacher_username, updated_teacher)
    if not teacher:
        raise HTTPException(status_code=409, detail="Teacher does not exists")
    return teacher