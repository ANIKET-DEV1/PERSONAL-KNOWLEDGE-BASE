from fastapi import APIRouter,Depends,HTTPException,status,Response
from sqlalchemy.orm import Session
from app.database.schemas.note import NoteCreate,NoteUpdate,NoteOut
from app.database.CRUD.note import Notecreate,UpdateUnote,delete_note
from app.JWT import get_curr_user
from app.database.db import get_db
from app.database.models.models import Note,User
note=APIRouter(prefix="/notes", tags=["Notes"])

@note.post("/add")
def createnote(
    New_Note: NoteCreate,
    db: Session = Depends(get_db),
    curr_user: User = Depends(get_curr_user),
):
    db_note = Notecreate(db, New_Note, curr_user.id)
    if not db_note:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Note creation failed",
        )
    return {"message": "Note Created"}

@note.put("/update")
def updateNote(updateNote:NoteUpdate,
               NoteID:int,
               db:Session=Depends(get_db),
                curr_user: User =Depends(get_curr_user)
):

    db_note=UpdateUnote(db,NoteID,updateNote,curr_user.id)
    if not db_note:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Note creation failed",
        )
    return {"message": "Note Created"}

@note.get("/view")
def get(db:Session=Depends(get_db),curr_user: User =Depends(get_curr_user)):
    return db.query(Note).filter(Note.user_id == curr_user.id).all()

@note.delete("/delete/{NoteID}")
def deletenot(NoteID:int,db:Session=Depends(get_db),curr_user: User=Depends(get_curr_user)):
    success= delete_note(db,NoteID,curr_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Note not found"
        )
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
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