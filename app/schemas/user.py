from pydantic import BaseModel,EmailStr
from datetime import date

class UserCreate(BaseModel):
    name:str
    email_id:EmailStr
    password:str

class UserLogin(BaseModel):
    email:EmailStr
    password:str

class UserOut(BaseModel):
    id:int
    name:str
    email:EmailStr
    create_at:date
