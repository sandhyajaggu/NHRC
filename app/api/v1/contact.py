from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.contact import ContactCreate
from app.services.contact_service import ContactService

router = APIRouter(
    prefix="/contact",
    tags=["Contact"]
)


@router.post("/")
def save_contact(
    payload: ContactCreate,
    db: Session = Depends(get_db)
):
    return ContactService.create_message(
        db,
        payload
    )