# app/api/v1/contact.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user
from app.models.member import Member
from app.schemas.contact import ContactCreate
from app.services.contact_service import ContactService
from app.db.session import get_db

router = APIRouter(prefix="/contact", tags=["Contact"])


# CREATE (already exists)
@router.post("/")
def create_contact(
    payload: ContactCreate,
    db: Session = Depends(get_db),
    user: Member = Depends(get_current_user)  # 🔥 important
):
    contact_data = payload.dict()

    #  auto assign membership_id
    contact_data["membership_id"] = user.membership_id

    return ContactService.create_contact(db, contact_data)

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