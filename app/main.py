from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from . import models
from .routers import(
    auth_routers, 
    user_routers, 
    google_auth 
) 

from .models import Chapter, Section, Lesson 
from sqlalchemy.event import listens_for
from .database import SessionLocal

models.Base.metadata.create_all(bind=engine)

@listens_for(Section, 'after_insert')
def receive_after_insert(mapper, connection, target):    
    db = SessionLocal()
    chapter = db.query(Chapter).filter(Chapter.chapter_name == target.chapter_name).first()
    if chapter:
        chapter.section_count = chapter.sections.count()
        db.commit()
    db.close()

@listens_for(Lesson, 'after_insert')
def receive_after_insert(mapper, connection, target):    
    db = SessionLocal()
    section = db.query(Section).filter(Section.section_name == target.section_name).first()
    if section:
        section.section_count = section.sections.count()
        db.commit()
    db.close()

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_routers.user_router)
app.include_router(auth_routers.auth_router)
app.include_router(google_auth.google_auth)