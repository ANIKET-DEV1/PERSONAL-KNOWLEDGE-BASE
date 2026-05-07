from pydantic import BaseModel,Field
from typing import Optional, List
from datetime import datetime
class NoteBase(BaseModel):
    title:str=Field(..., min_length=1, max_length=200)
    content:str=Field(..., min_length=1, max_length=50000)
    tags:Optional[str] = Field(None, description="Comma-separated tags")
    
class NoteCreate(NoteBase):
    is_archived:bool= Field(default=False)

class NoteUpdate(BaseModel):
    title:Optional[str]=Field(None, min_length=1, max_length=200)
    content:Optional[str]=Field(None, min_length=1, max_length=50000)
    tags:Optional[str]=None
    is_archived:Optional[bool]=Field(default=False)

class NoteOut(NoteBase):
    id:int
    user_id:int
    is_archived:bool
    created_at:datetime
    updated_at:datetime