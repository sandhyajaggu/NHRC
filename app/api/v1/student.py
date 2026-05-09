from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.schemas import job

from app.services.job_service import JobService
from app.services.job_application_service import (
    JobApplicationService
)

router = APIRouter(
    prefix="/student/jobs",
    tags=["Student"]
)


@router.get("/")
def get_jobs(
    db: Session = Depends(get_db)
):

    return JobService.get_all_jobs(db)


@router.get("/{job_id}")
def get_job_details(
    job_id: int,
    db: Session = Depends(get_db)
):

    return JobService.get_job_details(
        db,
        job_id
    )


@router.post("/apply")
def apply_job(
    payload: job.ApplyJobRequest,
    db: Session = Depends(get_db)
):

    return JobService.apply_job(
        db,
        payload
    )


@router.get("/applications/{membership_id}")
def get_my_applications(
    membership_id: str,
    db: Session = Depends(get_db)
):

    return JobApplicationService.get_student_applications(
        db,
        membership_id
    )