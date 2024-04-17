from fastapi import APIRouter, Depends,  HTTPException, status
from jose import JWTError, jwt
from typing import Annotated
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from ..crud.user_crud import get_user, create_user
from ..schemas.user_schemas import User, UserCreate
from ..schemas.token_schemas import TokenData
from ..crud.user_crud import get_user, get_user_by_email
from ..database import get_db
from .auth_routers import oauth2_scheme
import uuid
import os 

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
    print(user.full_name , user.email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    print(current_user.disabled)
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


@user_router.get("/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.id}]