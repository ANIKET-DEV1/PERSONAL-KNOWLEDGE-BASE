from fastapi import FastAPI,Path,HTTPException,routing,status,Depends
from sqlalchemy.orm import Session
from .database.db import get_db
from .database.schemas.user import UserCreate,UserLogin,UserOut
from .database.schemas.note import NoteCreate,NoteUpdate,NoteOut
from .database.schemas.auth import TokenData,Token
from .database.CRUD.crud import register_user,Authentitacate
from .auth import verify_token,get_curr_user,create_access_token
from app.config.app_config import getAppconfig
app= FastAPI()
items=[]
@app.get("/")
def root():
    config= getAppconfig()
    return {"app_name":config.app_name,
            "database_url":config.database_url}

@app.post("/register",response_model=Token, 
    status_code=status.HTTP_201_CREATED,
    tags=["Authentication"])
def register(user:UserCreate,db:Session = Depends(get_db)):
    db_user = register_user(db=db,user=user)
    token_payload = {"sub": str(db_user.id)}
    access_token = create_access_token(data=token_payload)
    return {"access_token": access_token, "token_type": "bearer"}



@app.post("/login",response_model=Token)
def login(cred:UserLogin,db:Session=Depends(get_db)):
    user=Authentitacate(db=db,cred=cred)
    if not user:
        raise HTTPException(status_code=403,detail="Invalid Crendential")
    token={"sub":str(user.id)}
    access_token=create_access_token(data=token)

    return {"access_token": access_token, "token_type": "bearer"}
