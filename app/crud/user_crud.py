import uuid
from sqlalchemy.orm import Session
from app import models
from ..utilities import verify_password ,get_password_hash
from ..schemas import user_schemas
from ..models import User, Lesson, Section, Chapter


def create_user(db: Session, user: user_schemas.UserCreate):
    user.password = get_password_hash(user.password)
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db_user.password = None
    return db_user

def get_user(db: Session, user_id: uuid.UUID ):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, user_email: str):
    return db.query(User).filter(User.email == user_email).first()

# username istead of email just for respecting the OpenAPI specs
def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_email(db, user_email=username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def move_to_next_lesson(db:Session, user_id: uuid.UUID):
    user = get_user(db, user_id)
    lesson = db.query(Lesson).filter(Lesson.lesson_name == user.current_lvl).first()
    if( not lesson):
        return user 
    next_lesson = db.query(Lesson).filter(Lesson.section_name == lesson.section_name , Lesson.order_in_section == lesson.order_in_section + 1 ).first()
    if (next_lesson): # there is another lesson in section 
        user.current_lvl = next_lesson.lesson_name
        db.commit()
        db.refresh(user)
        return user 
    
    section = db.query(Section).filter(Section.section_name == lesson.section_name).first()
    next_section = db.query(Section).filter(Section.chapter_name == section.chapter_name, Section.order_in_chapter == section.order_in_chapter + 1).first()        
    if (next_section): # there is another lesson in section 
        next_lesson = db.query(Lesson).filter(Lesson.section_name == next_section.section_name, Lesson.order_in_section == 1).first()
        user.current_lvl = next_lesson.lesson_name
        db.commit()
        db.refresh(user)
        return user 
       
    chapter = db.query(Chapter).filter(Chapter.chapter_name == section.chapter_name).first()
    next_chapter = db.query(Chapter).filter(Chapter.order == chapter.order +1).first()
    if(next_chapter):
        next_section = db.query(Section).filter(Section.chapter_name == next_chapter.chapter_name , Section.order_in_chapter == 1).first()
        next_lesson = db.query(Lesson).filter(Lesson.section_name == next_section.section_name, Lesson.order_in_section == 1).first()
        user.current_lvl = next_lesson.lesson_name
        db.commit()
        db.refresh(user)
        return user 
    
    user.current_lvl = "Sibawayh"
    db.commit()
    db.refresh(user)
    return user 