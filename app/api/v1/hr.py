from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.job import JobCreate, JobUpdate
from app.models.job import Job
from app.core.security import get_current_hr

router = APIRouter(
    prefix="/hr",
    tags=["HR"]
)

@router.post("/create")
def create_hr_job(
    payload: JobCreate,
    db: Session = Depends(get_db),
    hr = Depends(get_current_hr)
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
        "job": job
    }

@router.put("/update/{job_id}")
def update_hr_job(
    job_id: int,
    payload: JobUpdate,
    db: Session = Depends(get_db),
    hr = Depends(get_current_hr)
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
        "job_id": job.id
    }

@router.delete("/delete/{job_id}")
def delete_hr_job():

    raise HTTPException(
        status_code=403,
        detail="HR Does Not Have Delete Permission"
    )