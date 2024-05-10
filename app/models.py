from sqlalchemy import( 
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    UUID, 
    DateTime, 
    UniqueConstraint, 
    func 
)

from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.event import listens_for
from .database import Base, SessionLocal
import uuid

class User(Base):
    __tablename__='users'

    id= Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    email= Column(String(320), unique=True, index=True, nullable=False)  
    password= Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    completed_test = Column(Boolean, default=False)
    disabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    


class Chapter(Base):
    __tablename__ = "chapters"

    chpater_name=Column(String, index=True, primary_key=True)
    sections_count=Column(Integer, default=0) 

class Section(Base):
    __tablename__ = "sections"
  
    section_name = Column(String, index=True, primary_key=True)
    chpater_name = Column(String, ForeignKey("chapters.chpater_name"))
    order_in_chapter= Column(Integer)
    lessons_count=Column(Integer, default=0) 

    __table_args__ = (
        UniqueConstraint('chpater_name', 'order_in_chapter', name='_sections_order_uc'),
    )

class Lesson(Base):
    __tablename__ = "lessons"
    
    lesson_name = Column(String, index=True, primary_key=True)
    section_name = Column(String, ForeignKey("sections.section_name"))
    order_in_section= Column(Integer)

    __table_args__ = (
        UniqueConstraint('section_name', 'order_in_section', name='_lessons_order_uc'),
    )

class Quesion(Base):
    __tablename__ = "questions"

    id= Column(UUID, primary_key=True, default=uuid.uuid4)
    question= Column(String, nullable=False)
    lesson_name = Column(String, ForeignKey("lessons.lesson_name"))


class MCQ(Base):
    __tablename__ = "multiple_choice_questions"

    id= Column(UUID, ForeignKey("questions.id"), primary_key=True)
    answer= Column(String, nullable=False)
    option1 = Column(String, nullable=False)
    option2 = Column(String, nullable=False)
    option3 = Column(String, nullable=False)

class Iaarab(Base):
    __tablename__ = "iaarab_questions"

    id= Column(UUID, ForeignKey("questions.id"), primary_key=True)
    answer= Column(String, nullable=False)
    
class Writing(Base):
    __tablename__ = "writing_questions"

    id= Column(UUID, ForeignKey("questions.id"), primary_key=True)

class History(Base):
    __tablename__ = "history"
    user_id =Column(UUID, ForeignKey("users.id"), primary_key=True)
    question_id= Column(UUID, ForeignKey("questions.id"), primary_key=True)
    user_answer=Column(String, nullable=False)
    feedback=Column(String, nullable=False)
    date=Column(DateTime,default=func.now())

# @event.listens_for(Section.__table__, "after_insert")
# def update_section_count(mapper, connection, target, db: Session = Depends(get_db)):

#     chapter = db.query(Chapter).filter(Chapter.chapter_name == target.chapter_name).first()
#     if chapter:
#         chapter.section_count = chapter.sections.count()
#         db.commit()
#     db.close()

# @event.listens_for(Lesson.__table__, "after_insert")
# def update_section_count(mapper, connection, target, db: Session = Depends(get_db)):

#     section = db.query(Section).filter(Section.section_name == target.section_name).first()
#     if section:
#         section.section_count = section.sections.count()
#         db.commit()
#     db.close()

