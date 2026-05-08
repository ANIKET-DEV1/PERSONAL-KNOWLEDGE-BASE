from fastapi import FastAPI,Path,HTTPException,status,Depends,APIRouter
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.database.schemas.user import UserCreate,UserLogin,UserOut
from app.database.models.models import User
from app.database.schemas.auth import TokenData,Token
from app.JWT import get_curr_user
from app.database.CRUD.auth import register_user,Authentitacate

user=APIRouter(prefix="/user",tags=["User"])

@user.get("/profile" , response_model=UserOut)
def view_user(current_user: User = Depends(get_curr_user)):
    return current_user