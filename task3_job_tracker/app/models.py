from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List
from enum import Enum


class ApplicationStatus(str, Enum):
    """Job application status enum"""
    APPLIED = "applied"
    INTERVIEW = "interview"
    OFFER = "offer"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"


class User(SQLModel, table=True):
    """User model for database"""
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    applications: List["JobApplication"] = Relationship(back_populates="user")


class JobApplication(SQLModel, table=True):
    """Job application model for database"""
    id: Optional[int] = Field(default=None, primary_key=True)
    company: str = Field(index=True)
    position: str = Field(index=True)
    status: ApplicationStatus = Field(default=ApplicationStatus.APPLIED, index=True)
    application_date: datetime = Field(default_factory=datetime.utcnow)
    description: Optional[str] = None
    notes: Optional[str] = None
    user_id: int = Field(foreign_key="user.id")

    # Relationship
    user: User = Relationship(back_populates="applications")


# Pydantic models for API
class UserCreate(BaseModel):
    """User creation model"""
    username: str
    email: EmailStr
    password: str


class UserRead(BaseModel):
    """User response model"""
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime


class JobApplicationCreate(BaseModel):
    """Job application creation model"""
    company: str
    position: str
    status: ApplicationStatus = ApplicationStatus.APPLIED
    description: Optional[str] = None
    notes: Optional[str] = None


class JobApplicationUpdate(BaseModel):
    """Job application update model"""
    company: Optional[str] = None
    position: Optional[str] = None
    status: Optional[ApplicationStatus] = None
    description: Optional[str] = None
    notes: Optional[str] = None


class JobApplicationRead(BaseModel):
    """Job application response model"""
    id: int
    company: str
    position: str
    status: ApplicationStatus
    application_date: datetime
    description: Optional[str] = None
    notes: Optional[str] = None
    user_id: int


class Token(BaseModel):
    """Access token model"""
    access_token: str
    token_type: str


class LoginRequest(BaseModel):
    """Login request model"""
    username: str
    password: str
