from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime


class UserBase(SQLModel):
    username: str
    email: str


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    contacts: List["Contact"] = Relationship(back_populates="user")


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    created_at: datetime


class ContactBase(SQLModel):
    name: str
    email: str
    phone: str
    user_id: int = Field(foreign_key="user.id")


class Contact(ContactBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    user: Optional[User] = Relationship(back_populates="contacts")


class ContactCreate(SQLModel):
    name: str
    email: str
    phone: str


class ContactUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None


class ContactRead(ContactBase):
    id: int
    created_at: datetime
    updated_at: datetime


class Token(SQLModel):
    access_token: str
    token_type: str


class LoginRequest(SQLModel):
    username: str
    password: str


# Update forward references
UserRead.model_rebuild()
ContactRead.model_rebuild()
