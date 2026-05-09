from fastapi import APIRouter,Depends,HTTPException,status,Response, Query
from sqlalchemy.orm import Session
from app.database.schemas.note import NoteCreate,NoteUpdate,NoteOut
from app.database.CRUD.note import create_note, update_note, delete_note
from app.JWT import get_curr_user
from app.database.db import get_db
from app.database.models.models import Note,User
note=APIRouter(prefix="/notes", tags=["Notes"])

@note.post("", response_model=NoteOut, status_code=status.HTTP_201_CREATED)
def create_note_route(
    new_note: NoteCreate,
    db: Session = Depends(get_db),
    curr_user: User = Depends(get_curr_user),
):
    return create_note(db, new_note, curr_user.id)

@note.put("/{note_id}", response_model=NoteOut)
def update_note_route(update_note_payload: NoteUpdate,
               note_id:int,
               db:Session=Depends(get_db),
                curr_user: User =Depends(get_curr_user)
):
    return update_note(db, note_id, update_note_payload, curr_user.id)

@note.get("", response_model=list[NoteOut])
def get(db:Session=Depends(get_db),curr_user: User =Depends(get_curr_user)):
    return db.query(Note).filter(Note.user_id == curr_user.id).all()

@note.delete("/{note_id}")
def deletenot(note_id:int,db:Session=Depends(get_db),curr_user: User=Depends(get_curr_user)):
    success= delete_note(db,note_id,curr_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Note not found"
        )
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
@note.get("/search", response_model=list[NoteOut])
def search_notes(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_curr_user),
):
    return db.query(Note).filter(
        Note.user_id == current_user.id,
        (Note.title.ilike(f"%{q}%")) | (Note.content.ilike(f"%{q}%"))
    ).all()

@note.get("/{note_id}", response_model=NoteOut)
def get_single_note(
    note_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_curr_user)
):
    
    note = db.query(Note).filter(Note.id == note_id, Note.user_id == current_user.id).first()
    
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Note not found"
        )
    return note
