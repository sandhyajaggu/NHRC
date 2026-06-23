import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_student, get_current_user
from app.models.job import Job
from app.models.job_application import JobApplication
from app.models.job_fair import JobFair
from app.models.member import Member
from app.models.service_event import ServiceEvent
from app.models.student import StudentAutonomousDetails, StudentUniversityDetails
from app.models.student_job_fair_registration import StudentJobFairRegistration
from app.models.training_registration import TrainingRegistration
from app.models.user import User
from app.schemas.job_application import ApplyJobSchema
from app.schemas.job_fair_registration import StudentJobFairRegistrationCreate, StudentJobFairRegistrationResponse
from app.schemas.jobfair import JobFairResponse
from app.schemas.registration import RegistrationCreate
from app.schemas.student import StudentProfileUpdate
from app.schemas.training_registration_create import TrainingRegistrationCreate
from app.services.event_service import EventService
from app.services.registration_service import RegistrationService
from app.models.training_program import TrainingProgram
router = APIRouter(
    prefix="/student",
    tags=["STUDENT"]
)

@router.get("/profile")
def get_student_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Get member record using membership_id from JWT
    member = db.query(Member).filter(
        Member.membership_id == current_user.membership_id
    ).first()

    if not member:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )

    # Check university student
    university_student = db.query(StudentUniversityDetails).filter(
        StudentUniversityDetails.member_id == member.id
    ).first()

    if university_student:
        return {
            "success": True,
            "student_type": "university",
            "data": {
                "membership_id": member.membership_id,
                "email": university_student.email,
                "university_name": university_student.university_name,
                "college_name": university_student.college_name,
                "college_code": university_student.college_code,
                "qualification": university_student.qualification,
                "department": university_student.department,
                "start_year": university_student.start_year,
                "end_year": university_student.end_year,
                "location": university_student.location,
                "id_front": university_student.id_front,
                "id_back": university_student.id_back
            }
        }

    # Check autonomous student
    autonomous_student = db.query(StudentAutonomousDetails).filter(
        StudentAutonomousDetails.member_id == member.id
    ).first()

    if autonomous_student:
        return {
            "success": True,
            "student_type": "autonomous",
            "data": {
                "membership_id": member.membership_id,
                "email": autonomous_student.email,
                "college_name": autonomous_student.college_name,
                "college_code": autonomous_student.college_code,
                "qualification": autonomous_student.qualification,
                "department": autonomous_student.department,
                "start_year": autonomous_student.start_year,
                "end_year": autonomous_student.end_year,
                "location": autonomous_student.location,
                "id_front": autonomous_student.id_front,
                "id_back": autonomous_student.id_back
            }
        }

    raise HTTPException(
        status_code=404,
        detail="Student profile not found"
    )

@router.put("/profile")
def update_student_profile(
    payload: StudentProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Get member record
    member = db.query(Member).filter(
        Member.membership_id == current_user.membership_id
    ).first()

    if not member:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )

    # Find university student
    student = db.query(StudentUniversityDetails).filter(
        StudentUniversityDetails.member_id == member.id
    ).first()

    student_type = "university"

    # If not found, find autonomous student
    if not student:
        student = db.query(StudentAutonomousDetails).filter(
            StudentAutonomousDetails.member_id == member.id
        ).first()

        student_type = "autonomous"

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student profile not found"
        )

    # Update only provided fields
    update_data = payload.model_dump(exclude_unset=True)

    # Prevent university_name update for autonomous students
    if student_type == "autonomous":
        update_data.pop("university_name", None)

    for field, value in update_data.items():
        setattr(student, field, value)

    db.commit()
    db.refresh(student)

    response_data = {
        "membership_id": member.membership_id,
        "email": student.email,
        "college_name": student.college_name,
        "college_code": student.college_code,
        "qualification": student.qualification,
        "department": student.department,
        "start_year": student.start_year,
        "end_year": student.end_year,
        "location": student.location
    }

    if student_type == "university":
        response_data["university_name"] = student.university_name

    return {
        "success": True,
        "message": "Student profile updated successfully",
        "student_type": student_type,
        "data": response_data
    }

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
@router.get("/my-applications")
def get_my_applications(
    db: Session = Depends(get_db),
    student=Depends(get_current_student)
):

    applications = (
        db.query(JobApplication, Job)
        .join(
            Job,
            Job.id == JobApplication.job_id
        )
        .filter(
            JobApplication.student_id == student.id
        )
        .all()
    )

    return {
    "student_id": student.id,
    "total_applications": len(applications),
    "applications": [
        {
            "application_id": application.id,
            "job_id": job.id,
            "job_title": job.title,
            "company_name": job.company_name,
            "location": job.location,
            "status": application.status,
            "applied_at": application.applied_at
        }
        for application, job in applications
    ]
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

