from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from . import models
from .routers import(
    google_auth,
    auth_routers, 
    teacher_routers,  
    user_routers
) 

from .models import Chapter, Section, Lesson 
from sqlalchemy.event import listens_for
from .database import SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(google_auth.google_auth)
app.include_router(user_routers.user_router)
app.include_router(auth_routers.auth_router)
app.include_router(teacher_routers.teacher_router)