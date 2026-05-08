from pydantic import BaseModel,EmailStr,Field,model_validator,ConfigDict
from datetime import datetime

class UserBase(BaseModel):
    name:str=Field(...,min_length=2,max_length=20,
                decription="Username" , examples=["AWSMX"])
    email_id:EmailStr=Field(...,min_length=10,max_length=50,description="Email here",examples=["AWSMX@gmail.com"])
    
class UserCreate(UserBase):
    password:str=Field(..., min_length=8, description="Plain text password")
    confirm_password:str=Field(..., min_length=8, description="Plain text password")
    @model_validator(mode='after')
    def check_passwords_match(self) -> "UserCreate":
        if self.password != self.confirm_password:
            raise ValueError('Passwords do not match')
        return self

class UserLogin(BaseModel):
    email_id:EmailStr=Field(...,min_length=10,max_length=50,description="Email here",examples=["AWSMX@gmail.com"])
    password:str=Field(..., min_length=8, description="Plain text password")
    

class UserOut(UserBase):
    id:int
    created_at:datetime
    model_config = ConfigDict(from_attributes=True)