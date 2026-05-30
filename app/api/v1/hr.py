from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.event_job_role import EventJobRole
from app.models.job_fair import JobFair
from app.models.service_event import ServiceEvent
from app.schemas.job import JobCreate, JobUpdate
from app.models.job import Job
from app.core.security import get_current_employee, get_current_user
from app.services.event_service import EventService
from app.services.job_service import JobService

router = APIRouter(
    prefix="/hr",
    tags=["HR"]
)

@router.get("/dashboard")
def hr_dashboard(
    db: Session = Depends(get_db),
    hr = Depends(get_current_employee)
):

    jobs = db.query(Job).filter(
        Job.created_by == hr.membership_id
    ).all()

    return {
        "membership_id": hr.membership_id,
        "total_jobs": len(jobs),
        "jobs": jobs
    }

@router.post("/create")
def create_hr_job(
    payload: JobCreate,
    db: Session = Depends(get_db),
    hr = Depends(get_current_employee)
):

    job = Job(
        **payload.dict(),

        created_by=hr.membership_id,
        creator_role="HR",

        status="PENDING",
        is_public=False
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return {
        "message": "Job Sent For Approval",

        "job": {
            "id": job.id,

            "title": job.title,
            "company_name": job.company_name,
            "department": job.department,

            "work_mode": job.work_mode,
            "roles_responsibilities": job.roles_responsibilities,
            "required_skills": job.required_skills,
            "qualification_required": job.qualification_required,

            "min_experience": job.min_experience,
            "max_experience": job.max_experience,

            "min_salary": job.min_salary,
            "max_salary": job.max_salary,

            "perks_benefits": job.perks_benefits,

            "location": job.location,
            "locality": job.locality,

            "openings": job.openings,

            "application_deadline": job.application_deadline,

            "whatsapp_number": job.whatsapp_number,

            "created_by": job.created_by,
            "creator_role": job.creator_role,

            "status": job.status,
            "is_public": job.is_public,

            "created_at": job.created_at
        }
    }

@router.put("/update/{job_id}")
def update_hr_job(
    job_id: int,
    payload: JobUpdate,
    db: Session = Depends(get_db),
    hr = Depends(get_current_employee)
):

    job = db.query(Job).filter(
        Job.id == job_id
    ).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job Not Found"
        )

    # HR CAN UPDATE ONLY OWN JOBS
    if job.created_by != hr.membership_id:
        raise HTTPException(
            status_code=403,
            detail="You Can Update Only Your Jobs"
        )

    # HR CANNOT UPDATE ADMIN JOBS
    if job.creator_role == "ADMIN":
        raise HTTPException(
            status_code=403,
            detail="Cannot Update Admin Jobs"
        )

    for key, value in payload.dict().items():
        setattr(job, key, value)

    # After HR updates again send for approval
    job.status = "PENDING"
    job.is_public = False

    db.commit()
    db.refresh(job)
    return {
        "message": "Job Updated And Sent For Approval",

        "job": {
            "id": job.id,

            "title": job.title,
            "company_name": job.company_name,
            "department": job.department,

            "work_mode": job.work_mode,
            "roles_responsibilities": job.roles_responsibilities,
            "required_skills": job.required_skills,
            "qualification_required": job.qualification_required,

            "min_experience": job.min_experience,
            "max_experience": job.max_experience,

            "min_salary": job.min_salary,
            "max_salary": job.max_salary,

            "perks_benefits": job.perks_benefits,

            "location": job.location,
            "locality": job.locality,

            "openings": job.openings,

            "application_deadline": job.application_deadline,

            "whatsapp_number": job.whatsapp_number,

            "created_by": job.created_by,
            "creator_role": job.creator_role,

            "status": job.status,
            "is_public": job.is_public,

            "created_at": job.created_at
        }
    }

@router.get("/my-jobs")
def get_my_jobs(
    db: Session = Depends(get_db),
    hr = Depends(get_current_employee)
):

    return JobService.get_my_jobs(
        db,
        hr.membership_id
    )

@router.get("/my-jobs/count")
def get_my_jobs_count(
    db: Session = Depends(get_db),
    hr = Depends(get_current_employee)
):

    count = db.query(
        func.count(Job.id)
    ).filter(
        Job.created_by == hr.membership_id
    ).scalar()

    return {
        "membership_id": hr.membership_id,
        "total_jobs": count
    }
    

@router.delete("/delete/{job_id}")
def delete_hr_job():

    raise HTTPException(
        status_code=403,
        detail="HR Does Not Have Delete Permission"
    )
@router.get("/events")
def get_events(
    db: Session = Depends(get_db)
):

    return db.query(ServiceEvent).all()


@router.get("/job-fairs")
def get_job_fairs(
    db: Session = Depends(get_db)
):

    fairs = db.query(JobFair).all()

    return [
        {
            "id": fair.id,
            "title": fair.title,
            "description": fair.description,
            "organizer_name": fair.organizer_name,
            "event_mode": fair.event_mode,
            "start_date": fair.start_date,
            "end_date": fair.end_date,
            "location": fair.location
        }
        for fair in fairs
    ]