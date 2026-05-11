from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.job import JobCreate
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