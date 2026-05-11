from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.job import Job
from app.models.job_application import JobApplication
from app.schemas.job_application import ApplyJobSchema

router = APIRouter(
    prefix="/student/jobs",
    tags=["STUDENT JOBS"]
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

@router.post("/apply/{job_id}")
def apply_job(
    job_id: int,
    payload: ApplyJobSchema,
    db: Session = Depends(get_db),
    student = Depends(get_current_user)
):

    already_applied = db.query(JobApplication).filter(
        JobApplication.job_id == job_id,
        JobApplication.student_id == student.id
    ).first()

    if already_applied:
        raise HTTPException(
            400,
            "Already Applied"
        )

    application = JobApplication(
        job_id=job_id,

        student_id=student.id,
        student_membership_id=student.membership_id,

        student_name=student.name,
        email=student.email,

        qualification=student.qualification,
        experience=student.experience,

        resume=payload.resume
    )

    db.add(application)
    db.commit()

    return {
        "message": "Applied Successfully"
    }
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