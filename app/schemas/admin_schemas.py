from pydantic import BaseModel, Field

class AdminBase(BaseModel):
    username: str

class AdminCreate(AdminBase):
    password: str = Field(..., min_length=8, max_length=50, pattern="[A-Za-z0-9@$!%*#?&]+")  

class AdminResponse(AdminBase):
    pass