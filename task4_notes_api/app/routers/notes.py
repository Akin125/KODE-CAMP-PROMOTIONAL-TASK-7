from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
import json
import os
from datetime import datetime
from ..models import Note, NoteCreate, NoteUpdate, NoteRead
from ..database import get_session

router = APIRouter(prefix="/notes", tags=["notes"])


def backup_notes_to_json(session: Session):
    """Save all notes to notes.json for backup"""
    notes = session.exec(select(Note)).all()
    notes_data = []

    for note in notes:
        note_dict = {
            "id": note.id,
            "title": note.title,
            "content": note.content,
            "created_at": note.created_at.isoformat(),
            "updated_at": note.updated_at.isoformat()
        }
        notes_data.append(note_dict)

    with open("notes.json", "w") as f:
        json.dump(notes_data, f, indent=2)


@router.post("/", response_model=NoteRead)
def create_note(
    note: NoteCreate,
    session: Session = Depends(get_session)
):
    """Create a new note"""
    db_note = Note(**note.dict())
    session.add(db_note)
    session.commit()
    session.refresh(db_note)

    # Backup to JSON
    backup_notes_to_json(session)

    return db_note


@router.get("/", response_model=List[NoteRead])
def get_notes(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
):
    """Get all notes"""
    notes = session.exec(select(Note).offset(skip).limit(limit)).all()
    return notes


@router.get("/{note_id}", response_model=NoteRead)
def get_note(
    note_id: int,
    session: Session = Depends(get_session)
):
    """Get a specific note by ID"""
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.put("/{note_id}", response_model=NoteRead)
def update_note(
    note_id: int,
    note_update: NoteUpdate,
    session: Session = Depends(get_session)
):
    """Update a note"""
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    note_data = note_update.dict(exclude_unset=True)
    for field, value in note_data.items():
        setattr(note, field, value)

    # Update the updated_at timestamp
    note.updated_at = datetime.utcnow()

    session.add(note)
    session.commit()
    session.refresh(note)

    # Backup to JSON
    backup_notes_to_json(session)

    return note


@router.delete("/{note_id}")
def delete_note(
    note_id: int,
    session: Session = Depends(get_session)
):
    """Delete a note"""
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    session.delete(note)
    session.commit()

    # Backup to JSON after deletion
    backup_notes_to_json(session)

    return {"message": "Note deleted successfully"}
