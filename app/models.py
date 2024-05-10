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
from .database import Base
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

