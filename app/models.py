from sqlalchemy import( 
    Boolean,
    CheckConstraint,
    Column,
    ForeignKey,
    ForeignKeyConstraint,
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
    disabled = Column(Boolean, default=False) # omba3d nzido confirm your email
    current_lvl=Column(String, ForeignKey("lessons.lesson_name"), default="lesson 1")
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def __str__(self):
        return f"{self.id} | {self.email} | {self.password} | {self.full_name} | {self.completed_test} | {self.disabled} | {self.current_lvl} | {self.created_at} | {self.updated_at}"


class Chapter(Base):
    __tablename__ = "chapters"

    chapter_name=Column(String, index=True, primary_key=True)
    order= Column(Integer, nullable=False, unique=True)
    sections_count=Column(Integer, default=0) 

class Section(Base):
    __tablename__ = "sections"
  
    section_name = Column(String, index=True, primary_key=True)
    chapter_name = Column(String, ForeignKey("chapters.chapter_name"))
    order_in_chapter= Column(Integer, nullable=False)
    lessons_count=Column(Integer, default=0) 

    __table_args__ = (
        UniqueConstraint('chapter_name', 'order_in_chapter', name='_sections_order_uc'),
    )

class Lesson(Base):
    __tablename__ = "lessons"
    
    lesson_name = Column(String, index=True, primary_key=True)
    section_name = Column(String, ForeignKey("sections.section_name"))
    order_in_section= Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint('section_name', 'order_in_section', name='_lessons_order_uc'),
    )

    def __str__(self):
        return f"{self.lesson_name} | {self.section_name} | {self.order_in_section} "


class Question(Base):
    __tablename__ = "questions"

    id= Column(UUID, primary_key=True, default=uuid.uuid4)
    body= Column(String, nullable=False)
    lesson_name = Column(String, ForeignKey("lessons.lesson_name"))
    difficulty = Column(String(6) ,nullable=False) 
    type = Column(String(7) ,nullable=False) 


    def __str__(self):
        return f"{self.id}  -  {self.body} -  {self.lesson_name} - {self.difficulty} - {self.type}"

    __table_args__ = (
        CheckConstraint(
            "difficulty IN ('easy', 'medium', 'hard')",
            name='check_difficulty'
        ),
        CheckConstraint(
            "type IN ('mcq', 'iraab', 'writing')",
            name='check_type'
        ),
    )


class MCQ(Base):
    __tablename__ = "multiple_choice_questions"

    id= Column(UUID,  primary_key=True)
    answer= Column(String, nullable=False)
    option1 = Column(String, nullable=False)
    option2 = Column(String, nullable=False)
    option3 = Column(String, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(
            ['id'], ['questions.id'], ondelete='CASCADE'
        ),
    )
    def __str__(self):
        return f"{self.id}  -  {self.answer} -  {self.option1} -  {self.option2} -  {self.option3}  "

class Iraab(Base):
    __tablename__ = "iraab_questions"

    id= Column(UUID, primary_key=True)
    answer= Column(String, nullable=False) # TODO: remove asnwer and add word iraab.
    segmentation= Column(String, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(
            ['id'], ['questions.id'], ondelete='CASCADE'
        ),
    )
    
class Writing(Base):
    __tablename__ = "writing_questions"

    id= Column(UUID,  primary_key=True)

    __table_args__ = (
        ForeignKeyConstraint(
            ['id'], ['questions.id'], ondelete='CASCADE'
        ),
    )

class History(Base): # add difficulty
    __tablename__ = "history"
    user_id =Column(UUID, ForeignKey("users.id"), primary_key=True)
    question_id= Column(UUID,  primary_key=True) 
    lesson_name = Column(String)
    user_answer=Column(String, nullable=False)
    feedback=Column(String, nullable=False)
    date=Column(DateTime,default=func.now())
    type = Column(String(7) ,nullable=False) 
     
    __table_args__ = (
        ForeignKeyConstraint(
            ['user_id'], ['users.id'], ondelete='CASCADE'
        ),
        ForeignKeyConstraint(
            ['question_id'], ['questions.id'], ondelete='CASCADE'
        ),
    )

class ReportedQuestion(Base):
    __tablename__ = "reported_questions"

    user_id = Column(UUID, primary_key=True)
    question_id = Column(UUID, primary_key=True)
    reason = Column(String)

    __table_args__ = (
        ForeignKeyConstraint(
            ['user_id'], ['users.id'], ondelete='CASCADE'
        ),
        ForeignKeyConstraint(
            ['question_id'], ['questions.id'], ondelete='CASCADE'
        ),
    )

class Teacher(Base):
    __tablename__ = "teachers"

    username = Column(String, primary_key=True)
    password = Column(String, nullable=False)

class Admin(Base):
    __tablename__ = "admins"

    username = Column(String, primary_key=True)
    password = Column(String, nullable=False)