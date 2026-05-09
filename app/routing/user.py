from fastapi import Depends,APIRouter
from app.database.schemas.user import UserOut
from app.database.models.models import User
from app.JWT import get_curr_user

user=APIRouter(prefix="/users",tags=["User"])

@user.get("/me" , response_model=UserOut)
def view_user(current_user: User = Depends(get_curr_user)):
    return current_user
