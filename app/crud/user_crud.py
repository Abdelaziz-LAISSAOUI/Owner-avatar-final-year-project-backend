from sqlalchemy.orm import Session
from app import models
from ..utilities import verify_password ,get_password_hash
from ..schemas import user_schemas


def create_user(db: Session, user: user_schemas.UserCreate):
    user.password = get_password_hash(user.password)
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db_user.password = None
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, user_email: str):
    return db.query(models.User).filter(models.User.email == user_email).first()

# username istead of email just for respecting the OpenAPI specs
def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_email(db, user_email=username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

