from fastapi import APIRouter
from sqlalchemy.orm import Session
from app.database.schemas.note import NoteCreate,NoteUpdate,NoteOut
from app.database.models.models import Note
note=APIRouter(prefix="/notes", tags=["Notes"])

@note.get()
def note(db:Session,note:NoteCreate,user_id:int):
    