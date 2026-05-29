from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.event_registration import EventRegistration

from app.schemas.registration import RegistrationCreate

router = APIRouter(
    prefix="/registrations",
    tags=["Registrations"]
)


@router.post("/register")
def register_event(
    payload: RegistrationCreate,
    db: Session = Depends(get_db)
):

    registration = EventRegistration(
        member_id=1,
        event_id=payload.event_id
    )

    db.add(registration)

    db.commit()

    db.refresh(registration)

    return registration
