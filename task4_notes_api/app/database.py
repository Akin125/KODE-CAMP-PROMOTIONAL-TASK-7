from sqlmodel import SQLModel, create_engine, Session
from typing import Generator

# Database configuration
DATABASE_URL = "sqlite:///./notes.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


def create_db_and_tables():
    """Create database and tables"""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Dependency to get database session"""
    with Session(engine) as session:
        yield session
