from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.board_member import BoardMember
from app.models.member import Member
from app.models.user import User
from app.services.admin_service import AdminService
from app.schemas.admin import *
from app.schemas.member import MemberStatusUpdate
from app.schemas.member import BulkDeleteRequest

from app.schemas.job import CreateJobRequest, ApplyJobRequest

from app.services.job_service import JobService
from app.services.job_application_service import JobApplicationService

from app.core.dependencies import (
    get_current_user,
    get_current_admin
)


from app.core.dependencies import get_current_admin  

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

# ================= DASHBOARD =================
@router.get("/dashboard")
def dashboard(
    db: Session = Depends(get_db),
    admin: Member = Depends(get_current_admin)
):
    return AdminService.dashboard_stats(db)


# ================= USERS =================
@router.get("/employees")
def get_employees(
    db: Session = Depends(get_db),
    admin: Member = Depends(get_current_admin)
):
    return AdminService.list_users(db, "employee")


@router.get("/students")
def get_students(
    db: Session = Depends(get_db),
    admin: Member = Depends(get_current_admin)  
):
    return AdminService.list_users(db, "student")


@router.get("/representatives")
def get_representatives(
    db: Session = Depends(get_db),
    admin: Member = Depends(get_current_admin)   
):
    return AdminService.list_users(db, "representative")

@router.get("/member/{membership_id}")
def get_member_full_details(
    membership_id: str,
    db: Session = Depends(get_db),
    admin: Member = Depends(get_current_admin)
):
    return AdminService.get_member_full_details(db, membership_id)


# ================= APPROVAL =================



@router.put("/members/{membership_id}/approve")
def approve_member(membership_id: str, db: Session = Depends(get_db)):
    return AdminService.approve_user(db, membership_id)


@router.put("/members/{membership_id}/reject")
def reject_member(membership_id: str, db: Session = Depends(get_db)):
    return AdminService.reject_user(db, membership_id)


@router.delete("/members/{membership_id}")
def delete_member(membership_id: str, db: Session = Depends(get_db)):
    return AdminService.delete_user(db, membership_id)


@router.post("/members/bulk-delete")
def bulk_delete_members(
    payload: BulkDeleteRequest,
    db: Session = Depends(get_db),
    admin: Member = Depends(get_current_admin)
):
    return AdminService.bulk_delete_members(db, payload.membership_ids)

#=================== JOBS ===========================================================


@router.post("/")
def create_job(
    payload: ApplyJobRequest,
    db: Session = Depends(get_db)
):

    return JobService.create_admin_job(
        db,
        payload
    )


@router.get("/")
def get_jobs(
    db: Session = Depends(get_db)
):

    return JobService.get_all_jobs(db)


@router.get("/pending")
def get_pending_jobs(
    db: Session = Depends(get_db)
):

    return JobService.get_pending_jobs(db)


@router.put("/{job_id}/approve")
def approve_job(
    job_id: int,
    db: Session = Depends(get_db)
):

    return JobService.approve_job(
        db,
        job_id
    )


@router.put("/{job_id}/reject")
def reject_job(
    job_id: int,
    db: Session = Depends(get_db)
):

    return JobService.reject_job(
        db,
        job_id
    )


@router.get("/{job_id}")
def get_job_details(
    job_id: int,
    db: Session = Depends(get_db)
):

    return JobService.get_job_details(
        db,
        job_id
    )


@router.get("/{job_id}/applications")
def get_job_applications(
    job_id: int,
    db: Session = Depends(get_db)
):

    return JobApplicationService.get_job_applications(
        db,
        job_id
    )


@router.put("/applications/{application_id}/shortlist")
def shortlist_application(
    application_id: int,
    db: Session = Depends(get_db)
):

    return JobApplicationService.shortlist_application(
        db,
        application_id
    )


@router.put("/applications/{application_id}/reject")
def reject_application(
    application_id: int,
    db: Session = Depends(get_db)
):

    return JobApplicationService.reject_application(
        db,
        application_id
    )
@router.delete("/{job_id}")
def delete_job(
    job_id: int,
    db: Session = Depends(get_db)
):

    return JobService.delete_job(
        db,
        job_id
    )

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
