from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime


class StudentBase(SQLModel):
    name: str
    age: int
    email: str


class Student(StudentBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    grades: List["Grade"] = Relationship(back_populates="student")


class StudentCreate(StudentBase):
    pass


class StudentUpdate(SQLModel):
    name: Optional[str] = None
    age: Optional[int] = None
    email: Optional[str] = None


class StudentRead(StudentBase):
    id: int
    grades: List["Grade"] = []


class GradeBase(SQLModel):
    subject: str
    score: float
    student_id: int = Field(foreign_key="student.id")


class Grade(GradeBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    student: Optional[Student] = Relationship(back_populates="grades")


class GradeCreate(GradeBase):
    pass


class GradeRead(GradeBase):
    id: int
    created_at: datetime


class UserBase(SQLModel):
    username: str
    email: str


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int


# Update forward references
StudentRead.model_rebuild()
