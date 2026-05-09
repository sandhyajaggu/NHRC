from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import get_current_user

from app.services.job_service import JobService
from app.services.job_application_service import JobApplicationService

router = APIRouter(
    prefix="/student",
    tags=["Student"]
)


# GET APPROVED JOBS
@router.get("/jobs")
def get_jobs(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return JobService.get_student_jobs(db)


# APPLY JOB
@router.post("/jobs/{job_id}/apply")
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


# MY APPLICATIONS
@router.get("/my-applications")
def my_applications(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return JobApplicationService.get_member_applications(
        db,
        current_user.membership_id
    )