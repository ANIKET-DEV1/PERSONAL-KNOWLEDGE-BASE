from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.database.models.models import Note,User
from fastapi import HTTPException,status
from app.database.schemas.note import NoteCreate,NoteUpdate,NoteOut
from app.database.models import models

def Notecreate(db:Session,createNote:NoteCreate,user_id:int):
    db_note=Note(
            title=createNote.title,
            content=createNote.content,
            tags=createNote.tags,
            is_archived=createNote.is_archived,
            user_id=user_id
    )
    try:
        db.add(db_note)
        db.commit()
        db.refresh(db_note)
        return True
    except:
        raise HTTPException(503,detail="failed to store Data")


def UpdateUnote(db:Session,NoteId:int,updateNote:NoteUpdate,user_id:int):
        res = db.query(Note).filter(Note.id == NoteId, Note.user_id == user_id).first()
        if res is None:
                raise HTTPException(404, detail="Note Not Found")

        if updateNote.title is not None:
                res.title = updateNote.title
        if updateNote.content is not None:
                res.content = updateNote.content
        if updateNote.tags is not None:
                res.tags = updateNote.tags
        if updateNote.is_archived is not None:
                res.is_archived = updateNote.is_archived

        try:
                db.commit()
                db.refresh(res)
                return True
        except:
                db.rollback()
                raise HTTPException(503, detail="failed to update Data")

def delete_note(db: Session, note_id: int, user_id: int):
    
    note = db.query(Note).filter(Note.id == note_id, Note.user_id == user_id).first()
    
    if not note:
        return False 

    db.delete(note)
    db.commit()
    return True