from sqlalchemy.orm import Session
from sqlalchemy import select
from app.schemas import user
from app.database.models import models
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class PasswordHasher:
    @staticmethod
    def hash(password: str) -> str:
        """Returns a salted bcrypt hash."""
        return pwd_context.hash(password)

    @staticmethod
    def verify(plain_password: str, hashed_password: str) -> bool:
        """Checks if the plain text matches the stored hash."""
        return pwd_context.verify(plain_password, hashed_password)
    

def register_user(db:Session,user:models.UserCreate):
    if db.execute(select(models.User).where(models.User.email==user.email_id)).scalar().first() is not None:
        return {"EMAIL_EXIST"}
    if db.execute(select(models.User).where(models.User.name==user.name)).scalar().first() is not None:
        return {"UserName_Exist"}

    db_user = models.User(
        name=user.name,
        email_id=user.email_id,
        hashed_password=PasswordHasher.hash(user.password)
    )
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return True
    except Exception as e:
        db.rollback()
        return False

# def Authentitacate(db:Session,email,password):
#     try:
