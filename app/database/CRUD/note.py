from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException,status
from app.database.schemas.note import NoteCreate,NoteUpdate,NoteOut
from app.database.models import models

def Notecreate(db:Session,Note:NoteCreate,user_id:int):
    db_note=Note(
        title=note.title,
        content=note.content,
        tag=note.tags,
        user=user_id
    )