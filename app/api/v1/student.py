import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_student, get_current_user
from app.models.job import Job
from app.models.job_application import JobApplication
from app.models.job_fair import JobFair
from app.models.service_event import ServiceEvent
from app.models.student_job_fair_registration import StudentJobFairRegistration
from app.models.training_registration import TrainingRegistration
from app.schemas.job_application import ApplyJobSchema
from app.schemas.job_fair_registration import StudentJobFairRegistrationCreate, StudentJobFairRegistrationResponse
from app.schemas.jobfair import JobFairResponse
from app.schemas.registration import RegistrationCreate
from app.schemas.training_registration_create import TrainingRegistrationCreate
from app.services.event_service import EventService
from app.services.registration_service import RegistrationService
from app.models.training_program import TrainingProgram
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
@router.get("/training-programs")
def get_training_programs(

    db: Session = Depends(get_db),

    current_user=Depends(get_current_user)

):

    return db.query(
        TrainingProgram
    ).filter(
        TrainingProgram.status == "OPEN"
    ).all()

@router.get(
    "/job-fairs/{job_fair_id}",
    response_model=JobFairResponse
)
def get_job_fair_by_id(
    job_fair_id: int,
    db: Session = Depends(get_db)
):
    job_fair = (
        db.query(JobFair)
        .filter(JobFair.id == job_fair_id)
        .first()
    )

    if not job_fair:
        raise HTTPException(
            status_code=404,
            detail="Job Fair not found"
        )

    return job_fair
@router.get("/training-program/{training_id}")
def get_training_program(

    training_id: int,

    db: Session = Depends(get_db),

    current_user=Depends(get_current_user)

):

    training = db.query(
        TrainingProgram
    ).filter(
        TrainingProgram.id == training_id
    ).first()

    if not training:

        raise HTTPException(
            status_code=404,
            detail="Training Program not found"
        )

    return training

@router.get("/my-training-registrations")
def my_training_registrations(

    db: Session = Depends(get_db),

    current_user=Depends(get_current_user)

):

    registrations = db.query(
        TrainingRegistration
    ).filter(
        TrainingRegistration.member_id == current_user.id
    ).all()

    return registrations

from app.models.job_fair import JobFair


@router.post(
    "/job-fairs/student/register",
    response_model=StudentJobFairRegistrationResponse
)
def register_student_for_job_fair(
    payload: StudentJobFairRegistrationCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    job_fair = (
        db.query(JobFair)
        .filter(JobFair.id == payload.job_fair_id)
        .first()
    )

    if not job_fair:
        raise HTTPException(
            status_code=404,
            detail="Job Fair not found"
        )

    registration = StudentJobFairRegistration(
        **payload.model_dump()
    )

    db.add(registration)
    db.commit()
    db.refresh(registration)

    return registration

@router.get("/student/job-fairs/my-registrations")
def get_my_job_fair_registrations(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    registrations = (
        db.query(StudentJobFairRegistration)
        .filter(
            StudentJobFairRegistration.email == current_user.email
        )
        .all()
    )

    result = []

    for reg in registrations:

        job_fair = (
            db.query(JobFair)
            .filter(
                JobFair.id == reg.job_fair_id
            )
            .first()
        )

        if job_fair:
            result.append({
                "registration_id": reg.id,
                "job_fair_id": job_fair.id,
                "title": job_fair.title,
                "organization_name": job_fair.organization_name,
                "start_date": job_fair.start_date,
                "end_date": job_fair.end_date,
                "location": job_fair.location,
                "registered_on": reg.created_at
            })

    return result

