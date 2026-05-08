from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.schemas.job import JobCreate

from app.services.job_service import JobService
from app.services.job_application_service import JobApplicationService

from app.core.dependencies import (
    get_current_user,
    get_current_admin
)

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)


@router.post("/")
def create_job(
    payload: JobCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return JobService.create_job(
        db,
        payload,
        current_user
    )


@router.get("/")
def get_all_jobs(
    db: Session = Depends(get_db)
):

    return JobService.get_all_jobs(db)


@router.get("/student")
def get_student_jobs(
    db: Session = Depends(get_db)
):

    return JobService.get_student_jobs(db)


@router.get("/{job_id}")
def get_job_by_id(
    job_id: int,
    db: Session = Depends(get_db)
):

    return JobService.get_job_by_id(
        db,
        job_id
    )


@router.put("/{job_id}/approve")
def approve_job(
    job_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):

    return JobService.approve_job(
        db,
        job_id
    )


@router.put("/{job_id}/reject")
def reject_job(
    job_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):

    return JobService.reject_job(
        db,
        job_id
    )


@router.post("/{job_id}/apply")
def apply_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return JobApplicationService.apply_job(
        db,
        job_id,
        current_user
    )


@router.get("/{job_id}/applications")
def get_job_applications(
    job_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):

    return JobApplicationService.get_job_applications(
        db,
        job_id
    )