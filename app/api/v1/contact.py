# app/api/v1/contact.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.contact import ContactCreate
from app.services.contact_service import ContactService
from app.db.session import get_db

router = APIRouter(prefix="/contact", tags=["Contact"])


# CREATE (already exists)
@router.post("/")
def create_contact(payload: ContactCreate, db: Session = Depends(get_db)):
    return ContactService.create_contact(db, payload)


#  GET ALL
@router.get("/")
def get_all_contacts(db: Session = Depends(get_db)):
    return ContactService.get_all_contacts(db)


#  GET BY MEMBERSHIP ID
@router.get("/{membership_id}")
def get_contact(membership_id: str, db: Session = Depends(get_db)):
    try:
        return ContactService.get_contact_by_membership_id(db, membership_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


#  DELETE BY MEMBERSHIP ID
@router.delete("/{membership_id}")
def delete_contact(membership_id: str, db: Session = Depends(get_db)):
    try:
        return ContactService.delete_contact(db, membership_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))