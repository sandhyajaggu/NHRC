from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.schemas.job import CreateJobRequest

from app.services.job_service import JobService

router = APIRouter(
    prefix="/hr",
    tags=["HR"]
)


# CREATE JOB
@router.post("/")
def create_job(
    payload: CreateJobRequest,
    db: Session = Depends(get_db)
):

    return JobService.create_hr_job(
        db,
        payload
    )


# GET MY JOBS
@router.get("/{membership_id}")
def get_my_jobs(
    membership_id: str,
    db: Session = Depends(get_db)
):

    return JobService.get_hr_jobs(
        db,
        membership_id
    )


# UPDATE JOB
@router.put("/{job_id}")
def update_job(
    job_id: int,
    payload: CreateJobRequest,
    db: Session = Depends(get_db)
):

    return JobService.update_job(
        db,
        job_id,
        payload
    )


# DELETE JOB
@router.delete("/{job_id}")
def delete_job(
    job_id: int,
    db: Session = Depends(get_db)
):

    return JobService.delete_job(
        db,
        job_id
    )


# JOB DETAILS
@router.get("/details/{job_id}")
def get_job_details(
    job_id: int,
    db: Session = Depends(get_db)
):

    return JobService.get_job_details(
        db,
        job_id
    )


# GET APPLICATIONS
@router.get("/{job_id}/applications")
def get_job_applications(
    job_id: int,
    db: Session = Depends(get_db)
):

    return JobService.get_job_applications(
        db,
        job_id
    )