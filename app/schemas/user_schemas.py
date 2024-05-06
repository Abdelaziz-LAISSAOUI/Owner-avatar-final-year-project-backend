from datetime import datetime
import uuid
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel): 
    email : EmailStr    
    full_name : str  = Field(min_length=1)

class UserWithPassword(UserBase):
    password: str

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=50, pattern="[A-Za-z0-9@$!%*#?&]+")  


class User(UserBase):
    id : uuid.UUID
    completed_test : bool  
    disabled : bool 
    created_at : datetime 
    updated_at : datetime  


