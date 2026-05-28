from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.registration import (
    RegisterEventSchema
)

from app.services.registration_service import (
    RegistrationService
)

router = APIRouter(
    prefix="/register",
    tags=["Registrations"]
)


@router.post("/")
def register_event(
    payload: RegisterEventSchema,
    db: Session = Depends(get_db)
):

    return RegistrationService.register(
        db,
        payload
    )