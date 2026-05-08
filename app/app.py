from fastapi import FastAPI,Path,HTTPException,routing,status,Depends
from sqlalchemy.orm import Session
from .database.db import get_db
from .database.schemas.user import UserCreate,UserLogin,UserOut
from .database.schemas.note import NoteCreate,NoteUpdate,NoteOut
from .database.schemas.auth import TokenData,Token
from .routing import auth,user
from .database.CRUD.auth import register_user,Authentitacate
from .JWT import verify_token,get_curr_user
from app.config.app_config import getAppconfig
app= FastAPI()
app.include_router(auth.auth)
app.include_router(user.user)
@app.get("/")
def root():
    config= getAppconfig()
    return {"app_name":config.app_name,
            "database_url":config.database_url}


