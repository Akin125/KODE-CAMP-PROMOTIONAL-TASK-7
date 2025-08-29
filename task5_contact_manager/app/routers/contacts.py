from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from datetime import datetime
from ..models import Contact, ContactCreate, ContactUpdate, ContactRead, User
from ..database import get_session
from ..auth import get_current_user

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.post("/", response_model=ContactRead)
def create_contact(
    contact: ContactCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Add new contact (only logged-in user)"""
    db_contact = Contact(
        **contact.dict(),
        user_id=current_user.id
    )
    session.add(db_contact)
    session.commit()
    session.refresh(db_contact)
    return db_contact


@router.get("/", response_model=List[ContactRead])
def get_contacts(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """List user's contacts"""
    contacts = session.exec(
        select(Contact)
        .where(Contact.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
    ).all()
    return contacts


@router.get("/{contact_id}", response_model=ContactRead)
def get_contact(
    contact_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get a specific contact"""
    contact = session.exec(
        select(Contact).where(
            Contact.id == contact_id,
            Contact.user_id == current_user.id
        )
    ).first()

    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    return contact


@router.put("/{contact_id}", response_model=ContactRead)
def update_contact(
    contact_id: int,
    contact_update: ContactUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Update contact"""
    contact = session.exec(
        select(Contact).where(
            Contact.id == contact_id,
            Contact.user_id == current_user.id
        )
    ).first()

    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    contact_data = contact_update.dict(exclude_unset=True)
    for field, value in contact_data.items():
        setattr(contact, field, value)

    # Update the updated_at timestamp
    contact.updated_at = datetime.utcnow()

    session.add(contact)
    session.commit()
    session.refresh(contact)
    return contact


@router.delete("/{contact_id}")
def delete_contact(
    contact_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Delete contact"""
    contact = session.exec(
        select(Contact).where(
            Contact.id == contact_id,
            Contact.user_id == current_user.id
        )
    ).first()

    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    session.delete(contact)
    session.commit()
    return {"message": "Contact deleted successfully"}


@router.get("/search/by-name")
def search_contacts_by_name(
    name: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Search contacts by name"""
    contacts = session.exec(
        select(Contact).where(
            Contact.user_id == current_user.id,
            Contact.name.contains(name)
        )
    ).all()
    return contacts


@router.get("/search/by-email")
def search_contacts_by_email(
    email: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Search contacts by email"""
    contacts = session.exec(
        select(Contact).where(
            Contact.user_id == current_user.id,
            Contact.email.contains(email)
        )
    ).all()
    return contacts
