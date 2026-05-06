# This file maps Existing Postgres Table to a Python class.

from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import String,ForeignKey,Text,Boolean,DateTime,BigInteger,func,Identity
from app.database.db import Base
from datetime import datetime
from typing import List


class User(Base):
    __tablename__="users"
    id:Mapped[int]=mapped_column(BigInteger,Identity(always=True),primary_key=True)
    name:Mapped[str]=mapped_column(String(20),nullable=False)
    email:Mapped[str]=mapped_column(String(30),nullable=False,unique=True)
    hashed_password:Mapped[str]=mapped_column(Text,nullable=False)
    created_at:Mapped[datetime]=mapped_column(server_default=func.now())

    notes: Mapped[List["Note"]] = relationship(back_populates="owner")

class Note(Base):
    __tablename__="notes"
    id:Mapped[int]=mapped_column(BigInteger,Identity(always=True),primary_key=True)
    user_id:Mapped[int]=mapped_column(ForeignKey("users.id"),nullable=False)
    title:Mapped[str]=mapped_column(String(200),nullable=False)
    tags:Mapped[str]=mapped_column(Text,nullable=True)
    is_archived: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(onupdate=func.now())

    owner: Mapped["User"] = relationship(back_populates="notes")
