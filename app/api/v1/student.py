from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_student, get_current_user
from app.models.job import Job
from app.models.job_application import JobApplication
from app.models.job_fair import JobFair
from app.models.service_event import ServiceEvent
from app.schemas.job_application import ApplyJobSchema
from app.schemas.registration import RegistrationCreate
from app.services.event_service import EventService
from app.services.registration_service import RegistrationService

router = APIRouter(
    prefix="/student",
    tags=["STUDENT"]
)

@router.get("/all")
def get_all_jobs(
    db: Session = Depends(get_db)
):

    jobs = db.query(Job).filter(
        Job.is_public == True,
        Job.status == "APPROVED"
    ).all()

    return jobs


@router.get("/preview/{job_id}")
def student_job_preview(
    job_id: int,
    db: Session = Depends(get_db)
):

    job = db.query(Job).filter(
        Job.id == job_id,
        Job.status == "APPROVED",
        Job.is_public == True
    ).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job Not Found"
        )

    return job

@router.post("/apply/{job_id}")
def apply_job(
    job_id: int,
    payload: ApplyJobSchema,
    db: Session = Depends(get_db),
    student = Depends(get_current_student)
):

    # =========================
    # CHECK JOB
    # =========================

    job = db.query(Job).filter(
        Job.id == job_id,
        Job.status == "APPROVED",
        Job.is_public == True
    ).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job Not Found"
        )

    # =========================
    # DUPLICATE APPLY CHECK
    # =========================

    already_applied = db.query(
        JobApplication
    ).filter(
        JobApplication.job_id == job_id,
        JobApplication.student_id == student.id
    ).first()

    if already_applied:
        raise HTTPException(
            status_code=400,
            detail="Already Applied"
        )

    # =========================
    # EXPERIENCE VALIDATION
    # =========================

    if (
        payload.experience_type.upper()
        == "EXPERIENCED"
    ):

        if not payload.experiences:
            raise HTTPException(
                status_code=400,
                detail="Experience Details Required"
            )

    # =========================
    # CREATE APPLICATION
    # =========================

    application = JobApplication(

        job_id=job_id,

        student_id=student.id,

        student_membership_id=student.membership_id,

        # PERSONAL INFO

        first_name=payload.first_name,
        last_name=payload.last_name,

        phone_number=payload.phone_number,

        email=payload.email,

        date_of_birth=payload.date_of_birth,

        gender=payload.gender,

        location=payload.location,

        pan_number=payload.pan_number,

        pan_card_file=payload.pan_card_file,

        resume_file=payload.resume_file,

        photo_file=payload.photo_file,

        linkedin_url=payload.linkedin_url,

        # EDUCATION

        highest_qualification=payload.highest_qualification,

        specialization=payload.specialization,

        university=payload.university,

        college=payload.college,

        year_of_passing=payload.year_of_passing,

        # JOB DETAILS

        position_applied_for=payload.position_applied_for,

        preferred_work_mode=payload.preferred_work_mode,

        key_skills=payload.key_skills,

        expected_salary=payload.expected_salary,

        why_hire_me=payload.why_hire_me,

        # EXPERIENCE

        experience_type=payload.experience_type,

        experiences=[
            exp.dict()
            for exp in payload.experiences
        ]
        if payload.experiences else []
    )

    db.add(application)

    db.commit()

    db.refresh(application)

    return {
        "message": "Applied Successfully",
        "application_id": application.id
    }
@router.get("/events")
def get_events(
    db: Session = Depends(get_db)
):

    return db.query(ServiceEvent).all()


@router.get("/job-fairs")
def get_job_fairs(
    db: Session = Depends(get_db)
):

    return db.query(JobFair).all()
