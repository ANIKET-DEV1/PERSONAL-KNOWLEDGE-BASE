from fastapi import FastAPI,Path,HTTPException,status,Depends,APIRouter
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.database.schemas.user import UserCreate,UserLogin,UserOut
from app.database.schemas.auth import TokenData,Token
from app.JWT import create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from app.database.CRUD.auth import register_user,Authentitacate


auth = APIRouter(prefix="/auth", tags=["Authentication"])

@auth.post("/register",response_model=Token, 
    status_code=status.HTTP_201_CREATED,
    tags=["Authentication"])
def register(user:UserCreate,db:Session = Depends(get_db)):
    db_user = register_user(db=db,user=user)
    token_payload = {"sub": str(db_user.id)}
    access_token = create_access_token(data=token_payload)
    return {"access_token": access_token, "token_type": "bearer"}



@auth.post("/login",response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)):
    user=Authentitacate(db=db,email_id=form_data.username,password=form_data.password)
    if not user:
        raise HTTPException(status_code=403,detail="Invalid Crendential")
    token={"sub":str(user.id)}
    access_token=create_access_token(data=token)

    return {"access_token": access_token, "token_type": "bearer"}

