from sqlalchemy import( 
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Date, 
    Text,
    UUID, 
    DateTime, 
    UniqueConstraint, 
    func 
)

# from sqlalchemy.orm import relationship
import uuid
from .database import Base


class User(Base):
    __tablename__='users'

    id= Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    email= Column(String(256), unique=True, index=True, nullable=False)
    password= Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    completed_test = Column(Boolean, default=False)
    disabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    


class Chapter(Base):
    __tablename__ = "chapters"

    chpater_name = Column(String, index=True, primary_key=True)



class Section(Base):
    __tablename__ = "sections"

    
    section_name = Column(String, index=True, primary_key=True)
    chpater_name = Column(String, ForeignKey("chapters.chpater_name"))
    order_in_chapter= Column(Integer)
    
    __table_args__ = (
        UniqueConstraint('chpater_name', 'order_in_chapter', name='_sections_order_uc'),
    )

class Course(Base):
    __tablename__ = "courses"

    
    course_name = Column(String, index=True, primary_key=True)
    section_name = Column(String, ForeignKey("sections.section_name"))
    order_in_section= Column(Integer)
    
    __table_args__ = (
        UniqueConstraint('section_name', 'order_in_section', name='_courses_order_uc'),
    )

class Lesson(Base):
    __tablename__ = "lessons"

    
    lesson_name = Column(String, index=True, primary_key=True)
    course_name = Column(String, ForeignKey("courses.course_name"))
    order_in_course= Column(Integer)
    
    __table_args__ = (
        UniqueConstraint('course_name', 'order_in_course', name='_lessons_order_uc'),
    )

class Quesion(Base):
    __tablename__ = "questions"

    id= Column(UUID, primary_key=True)
    question= Column(String, nullable=False)
    answer= Column(String, nullable=False)
    option1 = Column(String, nullable=False)
    option2 = Column(String, nullable=False)
    option3 = Column(String, nullable=False)




