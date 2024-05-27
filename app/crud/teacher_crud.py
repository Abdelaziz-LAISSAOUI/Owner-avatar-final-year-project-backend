from sqlalchemy.orm import Session
from ..models import Teacher 
from ..schemas.teacher_schemas import TeacherCreate, TeacherUpdate
from ..utilities import get_password_hash, verify_password
import uuid

def create_teacher(db: Session, teacher:TeacherCreate):
    teacher.password = get_password_hash(teacher.password)
    db_teacher = Teacher(**teacher.model_dump())
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher

def get_teachers(db: Session , skip:int= 0, limit:int =10):
    return db.query(Teacher.username).offset(skip).limit(limit).all()

def delete_teacher(db: Session, teacher_username: uuid.UUID):
    db_teacher = db.query(Teacher).filter(Teacher.username == teacher_username).first()
    if db_teacher:
        db.delete(db_teacher)
        db.commit()
        return db_teacher
    else: 
        return None
    
def update_teacher(db: Session, teacher_username: uuid.UUID, updated_teacher: TeacherUpdate):
    db_teacher  = db.query(Teacher).filter(Teacher.username == teacher_username).first()
    if db_teacher:
        for k, v in updated_teacher.model_dump().items():
            setattr(db_teacher, k, v)
        db.commit()
        db.refresh(db_teacher)
        return db_teacher
    else: 
        return None
    
def get_teacher(db: Session, username: str):
    return db.query(Teacher).filter(Teacher.username == username).first()

def authenticate_teacher(db: Session, username: str, password: str):
    teacher = get_teacher(db, username)
    if not teacher:
        return False
    if not verify_password(password, teacher.password):
        return False
    return teacher