from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException,status
from app.database.schemas.user import UserCreate,UserLogin
from app.database.models import models
import hashlib
import bcrypt

class PasswordHasher:
    @staticmethod
    def hash(password: str) -> str:
        """Hash password safely for bcrypt by pre-hashing to fixed length."""
        normalized = hashlib.sha256(password.encode("utf-8")).hexdigest().encode("utf-8")
        return bcrypt.hashpw(normalized, bcrypt.gensalt()).decode("utf-8")

    @staticmethod
    def verify(plain_password: str, hashed_password: str) -> bool:
        """Verify password against stored bcrypt hash."""
        normalized = hashlib.sha256(plain_password.encode("utf-8")).hexdigest().encode("utf-8")
        return bcrypt.checkpw(normalized, hashed_password.encode("utf-8"))
    

def register_user(db:Session,user:UserCreate):
    email_exists = db.execute(
        select(models.User.id).where(models.User.email_id == user.email_id)).scalars().first()
    userName_exist = db.execute(
        select(models.User.id).where(models.User.name == user.name)).scalars().first()
    if email_exists or userName_exist:
        raise(HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or username Exist"
        ))
    hashed_password=PasswordHasher.hash(user.password)
    db_user = models.User(
        name=user.name,
        email_id=user.email_id,
        hashed_password=hashed_password
    )
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists or invalid data for database constraints"
        )
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error occurred: {str(e.__class__.__name__)}"
        )

def Authentitacate(db:Session,email_id:str,password:str):
    user = db.execute(select(models.User).where(models.User.email_id == email_id)).scalars().first()
    print(user)
    if not user:
        return None
    
    if not PasswordHasher.verify(password, user.hashed_password):
        return None

    return user
