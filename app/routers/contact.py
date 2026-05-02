from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.contact import ContactCreate
from app.models.contact import ContactMessage

router = APIRouter(prefix="/contact", tags=["Contact"])

@router.post("/")
def save_contact(payload: ContactCreate, db: Session = Depends(get_db)):
    msg = ContactMessage(**payload.dict())
    db.add(msg)
    db.commit()
    return {"message": "Contact saved successfully"}