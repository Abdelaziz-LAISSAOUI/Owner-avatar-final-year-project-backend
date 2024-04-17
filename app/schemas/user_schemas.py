from datetime import datetime
import uuid
from pydantic import BaseModel 


class UserBase(BaseModel): 
    email : str    
    full_name : str  

class UserWithPassword(UserBase):
    password: str

class UserCreate(UserBase):
    password : str


class User(UserBase):
    id : uuid.UUID
    completed_test : bool  
    disabled : bool 
    created_at : datetime 
    updated_at : datetime  


