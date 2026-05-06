from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class NoteCreate(BaseModel):
    title:str
    content:str
    tags:Optional[List]  
    is_archived:bool

class NoteUpdate(BaseModel):
    title:Optional[str]
    content:Optional[str]
    tags:Optional[List]
    is_archived:Optional[bool]

class NoteOut(BaseModel):
    id:int
    user_id:int
    title:str
    content:str
    tags:Optional[List]
    is_archived:bool
    created_at:date
    updated_at:date