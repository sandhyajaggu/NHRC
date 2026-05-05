# app/api/v1/contact.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user
from app.models.member import Member
from app.schemas.contact import ContactCreate, ContactResponse
from app.services.contact_service import ContactService
from app.db.session import get_db

router = APIRouter(prefix="/contact", tags=["Contact"])


# CREATE (already exists)
@router.post("/", response_model=ContactResponse)
def create_contact(
    payload: ContactCreate,
    db: Session = Depends(get_db)
):
    contact_data = payload.dict()
    return ContactService.create_contact(db, contact_data)
#  GET ALL
@router.get("/")
def get_all_contacts(db: Session = Depends(get_db)):
    return ContactService.get_all_contacts(db)


#  GET BY MEMBERSHIP ID
@router.get("/{contact_id}")
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    return ContactService.get_contact_by_id(db, contact_id)


@router.delete("/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    return ContactService.delete_contact(db, contact_id)