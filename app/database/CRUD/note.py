from sqlalchemy.orm import Session
from app.database.models.models import Note
from fastapi import HTTPException
from app.database.schemas.note import NoteCreate, NoteUpdate

def create_note(db: Session, create_note_data: NoteCreate, user_id: int):
    db_note = Note(
            title=create_note_data.title,
            content=create_note_data.content,
            tags=create_note_data.tags,
            is_archived=create_note_data.is_archived,
            user_id=user_id
    )
    try:
        db.add(db_note)
        db.commit()
        db.refresh(db_note)
        return db_note
    except:
        db.rollback()
        raise HTTPException(503, detail="failed to store Data")


def update_note(db: Session, note_id: int, update_note_data: NoteUpdate, user_id: int):
        res = db.query(Note).filter(Note.id == note_id, Note.user_id == user_id).first()
        if res is None:
                raise HTTPException(404, detail="Note not found")

        if update_note_data.title is not None:
                res.title = update_note_data.title
        if update_note_data.content is not None:
                res.content = update_note_data.content
        if update_note_data.tags is not None:
                res.tags = update_note_data.tags
        if update_note_data.is_archived is not None:
                res.is_archived = update_note_data.is_archived

        try:
                db.commit()
                db.refresh(res)
                return res
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
