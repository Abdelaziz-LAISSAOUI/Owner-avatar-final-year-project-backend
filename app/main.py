from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from . import models
from .routers import(
    google_auth,
    auth_routers, 
    teacher_routers,  
    user_routers, 
    admin_routers, 
    reported_question_routers, 
    question_routers
) 

# from .models import Chapter, Section, Lesson 
# from sqlalchemy.event import listens_for
# from .database import SessionLocal

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
app.include_router(admin_routers.admin_router)
app.include_router(reported_question_routers.reported_question_router)
app.include_router(question_routers.question_router)
