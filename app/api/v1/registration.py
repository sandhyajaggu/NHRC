import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.models.event_registration import EventRegistration
from app.models.training import TrainingProgram
from app.models.training_registration import TrainingRegistration
from app.schemas.registration import RegistrationCreate
from app.schemas.training_registration_create import TrainingRegistrationCreate

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

    role = current_user.role.strip().upper()

    # ==================================
    # ONLY STUDENT & EMPLOYEE CAN REGISTER
    # ==================================

    if role not in ["STUDENT", "EMPLOYEE"]:
        raise HTTPException(
            status_code=403,
            detail="Only HR and Students can register"
        )

    # ==================================
    # EVENT OR JOB FAIR REQUIRED
    # ==================================

    if not payload.event_id and not payload.job_fair_id:
        raise HTTPException(
            status_code=400,
            detail="event_id or job_fair_id required"
        )

    # ==================================
    # STUDENT VALIDATION
    # ==================================

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

    # ==================================
    # HR VALIDATION
    # ==================================

    if role == "EMPLOYEE":

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

        # Save only HR or STUDENT
        member_type="HR" if role == "EMPLOYEE" else "STUDENT",

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
        "registration_id": registration.id,
        "member_type": registration.member_type
    }
@router.post("/training/register")
def register_training(

    payload: TrainingRegistrationCreate,

    db: Session = Depends(get_db),

    current_user=Depends(get_current_user)

):

    role = current_user.role.strip().upper()

    # Only Student and Employee

    if role not in ["STUDENT", "EMPLOYEE"]:

        raise HTTPException(
            status_code=403,
            detail="Only Student and HR can register"
        )

    training = db.query(
        TrainingProgram
    ).filter(
        TrainingProgram.id == payload.training_id
    ).first()

    if not training:

        raise HTTPException(
            status_code=404,
            detail="Training Program not found"
        )

    # Prevent Duplicate Registration

    existing = db.query(
        TrainingRegistration
    ).filter(
        TrainingRegistration.training_id == payload.training_id,
        TrainingRegistration.member_id == current_user.id
    ).first()

    if existing:

        raise HTTPException(
            status_code=400,
            detail="Already Registered"
        )

    # Student Validation

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

    # HR Validation

    if role == "EMPLOYEE":

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

    registration = TrainingRegistration(

        training_id=payload.training_id,

        member_id=current_user.id,

        member_type="HR" if role == "EMPLOYEE" else "STUDENT",

        full_name=payload.full_name,

        email=current_user.email,

        phone=payload.phone,

        location=payload.location,

        iam_a=payload.iam_a,

        nhrc_id=payload.nhrc_id,

        receive_updates=payload.receive_updates,

        college_name=payload.college_name,

        year_of_passout=payload.year_of_passout,

        company_name=payload.company_name,

        company_location=payload.company_location,

        status="REGISTERED",

        created_at=datetime.utcnow()
    )

    db.add(registration)

    db.commit()

    db.refresh(registration)

    return {
        "message": "Training Registration Successful",
        "registration_id": registration.id
    }
