from jose import jwt,JWTError
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from .database.db import get_db
from .database.models.models import User
from datetime import datetime, timedelta, timezone
from .database.schemas.auth import TokenData
from fastapi.security import OAuth2PasswordBearer
from .config.app_config import getAppconfig
system=getAppconfig()
SECRET_KEY = system.secret_key.get_secret_value()
ALGORITHM = system.algorithms
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def verify_token(token: str, credential_exception: HTTPException | None = None):
    if credential_exception is None:
        credential_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise credential_exception

        token_data = TokenData(user_id=user_id)
        return token_data
    except JWTError:
        raise credential_exception

def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.now(timezone.utc) + timedelta(
        minutes=system.ACCESS_TOKEN_EXPIRE_MINUTE
    )
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return encoded_jwt

def get_curr_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    token_data = verify_token(token)
    user = db.query(User).filter(User.id == token_data.user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user
