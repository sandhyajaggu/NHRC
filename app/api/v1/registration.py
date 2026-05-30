from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.core.security import get_current_user

from app.models.member import Member

from app.models.service_event import ServiceEvent

from app.models.job_fair import JobFair

from app.models.event_registration import EventRegistration

from app.schemas.registration import RegistrationCreate


router = APIRouter(
    prefix="/registrations",
    tags=["Registrations"]
)


@router.post("/register")
def register(
    payload: RegistrationCreate,
    db: Session = Depends(get_db),
    current_user: Member = Depends(get_current_user)
):

    # ==========================
    # VALIDATION
    # ==========================

    if not payload.event_id and not payload.job_fair_id:

        raise HTTPException(
            status_code=400,
            detail="event_id or job_fair_id required"
        )

    # ==========================
    # EVENT REGISTRATION
    # ==========================

    if payload.event_id:

        event = db.query(ServiceEvent).filter(
            ServiceEvent.id == payload.event_id
        ).first()

        if not event:

            raise HTTPException(
                status_code=404,
                detail="Event not found"
            )

        registration = EventRegistration(

            member_id=current_user.id,

            event_id=event.id,

            member_type=current_user.role,

            full_name=current_user.full_name,

            email=current_user.email,

            status="PENDING"
        )

        db.add(registration)

        db.commit()

        db.refresh(registration)

        return {
            "message": "Successfully registered for Event"
        }

    # ==========================
    # JOB FAIR REGISTRATION
    # ==========================

    if payload.job_fair_id:

        if current_user.role.strip().upper() == "EMPLOYEE":

            raise HTTPException(
                status_code=403,
                detail="HR cannot register for Job Fairs"
            )

        job_fair = db.query(JobFair).filter(
            JobFair.id == payload.job_fair_id
        ).first()

        if not job_fair:

            raise HTTPException(
                status_code=404,
                detail="Job Fair not found"
            )

        registration = EventRegistration(

            member_id=current_user.id,

            job_fair_id=job_fair.id,

            member_type=current_user.role,

            full_name=current_user.full_name,

            email=current_user.email,

            status="PENDING"
        )

        db.add(registration)

        db.commit()

        db.refresh(registration)

        return {
            "message": "Successfully registered for Job Fair"
        }