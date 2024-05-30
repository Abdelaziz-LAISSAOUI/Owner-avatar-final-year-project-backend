from fastapi import APIRouter, Depends,  HTTPException, Request, status
from jose import JWTError, jwt
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from ..database import get_db


from ..crud.admin_crud import get_admin, create_admin
from ..schemas.admin_schemas import AdminResponse, AdminCreate
from ..schemas.token_schemas import TokenData
import uuid
import os 


admin_router = APIRouter(
    prefix="/v1/admins",
    tags=["admins"],
)

load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')


async def is_admin(req: Request, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
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
    
    admin = get_admin(db, id)
    if admin is None:
        raise credentials_exception
    return admin



@admin_router.post("/", response_model=AdminResponse, status_code=201, responses={409: {"description": "Conflict"}})
async def create_new_admin(admin: AdminCreate, db: Session = Depends(get_db)):
    admin_exist = get_admin(db, username= admin.username)
    if admin_exist: 
        raise HTTPException(status_code=409, detail="Admin already exists")
    new_admin = create_admin(db, admin)
    return new_admin
