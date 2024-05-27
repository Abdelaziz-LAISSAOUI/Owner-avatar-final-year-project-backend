
from pydantic import BaseModel, Field

class TeacherBase(BaseModel):
    username: str

class TeacherCreate(BaseModel): 
    
    username : str
    password: str = Field(..., min_length=8, max_length=50, pattern="[A-Za-z0-9@$!%*#?&]+")  

class TeacherResponse(TeacherBase):
    pass 

class TeacherUpdate(TeacherBase):
    pass