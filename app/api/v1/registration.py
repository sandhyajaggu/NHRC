from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import APIRouter
from app.core.security import get_current_user
from app.db.session import get_db
from app.models.event_registration import EventRegistration
from app.schemas.registration import RegistrationCreate
router = APIRouter(
    prefix="/registration",
    tags=["Registration"]
)

@router.post("/register")
def register(
    payload: RegistrationCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    role = current_user.role.upper()

    # ==================
    # STUDENT VALIDATION
    # ==================

    if role == "STUDENT":

        if not payload.college_name:
            raise HTTPException(
                status_code=400,
                detail="college_name required"
            )

        if not payload.year_of_passout:
            raise HTTPException(
                status_code=400,
                detail="year_of_passout required"
            )

    # ==================
    # HR VALIDATION
    # ==================

    if role == "EMPLOYEE":

        if payload.job_fair_id:

            raise HTTPException(
                status_code=403,
                detail="HR cannot register for Job Fairs"
            )

        if not payload.company_name:
            raise HTTPException(
                status_code=400,
                detail="company_name required"
            )

        if not payload.company_location:
            raise HTTPException(
                status_code=400,
                detail="company_location required"
            )

    registration = EventRegistration(

        member_id=current_user.id,

        event_id=payload.event_id,

        job_fair_id=payload.job_fair_id,

        member_type=role,

        full_name=payload.full_name,

        email=current_user.email,

        phone=payload.phone,

        location=payload.location,

        iam_a=payload.iam_a,

        nhrc_id=payload.nhrc_id,

        college_name=payload.college_name,

        year_of_passout=payload.year_of_passout,

        company_name=payload.company_name,

        company_location=payload.company_location,

        receive_updates=payload.receive_updates,

        status="PENDING"
    )

    db.add(registration)

    db.commit()

    db.refresh(registration)

    return {
        "message": "Registration Successful",
        "registration_id": registration.id
    }