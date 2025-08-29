from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime
from pydantic import BaseModel


class NoteBase(SQLModel):
    title: str
    content: str


class Note(NoteBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class NoteCreate(NoteBase):
    pass


class NoteUpdate(SQLModel):
    title: Optional[str] = None
    content: Optional[str] = None


class NoteRead(NoteBase):
    id: int
    created_at: datetime
    updated_at: datetime


class RequestCountModel(BaseModel):
    total_requests: int
    last_updated: datetime
