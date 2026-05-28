from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.board_member import BoardMember
from app.models.job import Job
from app.models.job_application import JobApplication
from app.models.member import Member
from app.models.user import User
from app.schemas.job import JobCreate, JobUpdate
from app.services.admin_service import AdminService
from app.schemas.admin import *
from app.schemas.member import MemberStatusUpdate
from app.schemas.member import BulkDeleteRequest
from app.schemas.service_event import CreateEventSchema

from app.services.event_service import EventService
from app.services.registration_service import (
    RegistrationManagementService
)



from app.core.security import (
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

@router.post("/create")
def create_job(
    payload: JobCreate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):

    job = Job(
        **payload.dict(),

        created_by=admin.membership_id,
        creator_role="ADMIN",
        

        status="APPROVED",
        is_public=True
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return {
        "message": "Job created successfully",
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
            "whatsapp_number": job.whatsapp_number
        }
    }

@router.put("/approve/{job_id}")
def approve_job(
    job_id: int,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):

    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(404, "Job Not Found")
    # ADMIN JOBS CANNOT BE APPROVED AGAIN
    if job.creator_role == "ADMIN":
        raise HTTPException(
            status_code=400,
            detail="Admin Created Jobs Are Already Approved"
        )

    job.status = "APPROVED"
    job.is_public = True

    db.commit()

    return {
        "message": "Job Approved",
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
            "whatsapp_number": job.whatsapp_number
        }
    }

@router.put("/reject/{job_id}")
def reject_job(
    job_id: int,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):

    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(404, "Job Not Found")
    

    if job.creator_role == "ADMIN":
        raise HTTPException(
            403,
            "Admin Jobs Cannot Be Rejected"
        )

    job.status = "REJECTED"
    job.is_public = False

    db.commit()

    return {
        "message": "Job Rejecred",
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
            "whatsapp_number": job.whatsapp_number
        }
    }

@router.delete("/delete/{job_id}")
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):

    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(404, "Job Not Found")

    db.delete(job)
    db.commit()

    return {
        "message": "Job Deleted Successfully"
    }

@router.put("/update/{job_id}")
def update_job(
    job_id: int,
    payload: JobUpdate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):

    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(404, "Job Not Found")

    for key, value in payload.dict().items():
        setattr(job, key, value)

    db.commit()
    db.refresh(job)

    return {
        "message": "Job Updated",
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
            "whatsapp_number": job.whatsapp_number
        }
    }


@router.get("/{job_id}/applications")
def get_job_applications(
    job_id: int,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):

    applications = db.query(JobApplication).filter(
        JobApplication.job_id == job_id
    ).all()

    return applications

from sqlalchemy import func
from app.models.job_application import JobApplication

@router.get("/all")
def admin_all_jobs(
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):

    jobs = db.query(Job).all()

    response = []

    for job in jobs:

        total = db.query(JobApplication).filter(
            JobApplication.job_id == job.id
        ).count()

        shortlisted = db.query(JobApplication).filter(
            JobApplication.job_id == job.id,
            JobApplication.status == "SHORTLISTED"
        ).count()

        rejected = db.query(JobApplication).filter(
            JobApplication.job_id == job.id,
            JobApplication.status == "REJECTED"
        ).count()

        response.append({

            # BASIC INFO
            "job_id": job.id,
            "title": job.title,
            "company_name": job.company_name,
            "department": job.department,

            # JOB DETAILS
            "work_mode": job.work_mode,
            "roles_responsibilities": job.roles_responsibilities,
            "required_skills": job.required_skills,
            "qualification_required": job.qualification_required,

            # EXPERIENCE
            "min_experience": job.min_experience,
            "max_experience": job.max_experience,

            # SALARY
            "min_salary": job.min_salary,
            "max_salary": job.max_salary,

            # EXTRA DETAILS
            "perks_benefits": job.perks_benefits,
            "location": job.location,
            "locality": job.locality,
            "openings": job.openings,
            "application_deadline": job.application_deadline,
            "whatsapp_number": job.whatsapp_number,

            # CREATED INFO
            "created_by": job.created_by,
            "creator_role": job.creator_role,
            "status": job.status,
            "created_at": job.created_at,

            # APPLICATION COUNTS
            "all_responses": total,
            "shortlisted": shortlisted,
            "rejected": rejected
        })

    return response
@router.get("/preview/{job_id}")
def job_preview(
    job_id: int,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):

    job = db.query(Job).filter(
        Job.id == job_id
    ).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job Not Found"
        )
  
    return {
        "job_id": job.id,
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
        "status": job.status,
        "created_by": job.created_by,
        "creator_role": job.creator_role,
        "created_at": job.created_at
    }
from app.models.job_application import JobApplication

@router.put("/application/{application_id}/shortlist")
def shortlist_candidate(
    application_id: int,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):

    application = db.query(JobApplication).filter(
        JobApplication.id == application_id
    ).first()

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application Not Found"
        )

    application.status = "SHORTLISTED"

    db.commit()

    return {
        "message": "Candidate Shortlisted Successfully",
        "application_id": application.id,
        "student_membership_id": application.student_membership_id
    }

@router.put("/application/{application_id}/reject")
def reject_candidate(
    application_id: int,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):

    application = db.query(JobApplication).filter(
        JobApplication.id == application_id
    ).first()

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application Not Found"
        )

    application.status = "REJECTED"

    db.commit()

    return {
        "message": "Candidate Rejected Successfully",
        "application_id": application.id,
        "student_membership_id": application.student_membership_id
    }

@router.post("/create")
def create_event(
    payload: CreateEventSchema,
    db: Session = Depends(get_db)
):

    return EventService.create_event(db, payload)

@router.put("/approve/{registration_id}")
def approve_registration(
    registration_id: int,
    db: Session = Depends(get_db)
):

    return RegistrationManagementService.approve_registration(
        db,
        registration_id
    )

@router.put("/approve/{registration_id}")
def approve_registration(
    registration_id: int,
    db: Session = Depends(get_db)
):

    return RegistrationManagementService.approve_registration(
        db,
        registration_id
    )

@router.put("/reject/{registration_id}")
def reject_registration(
    registration_id: int,
    db: Session = Depends(get_db)
):

    return RegistrationManagementService.reject_registration(
        db,
        registration_id
    )

@router.put("/forward/{registration_id}")
def forward_registration(
    registration_id: int,
    forwarded_to: str,
    db: Session = Depends(get_db)
):

    return RegistrationManagementService.forward_registration(
        db,
        registration_id,
        forwarded_to
    )
@router.delete("/{event_id}")
def delete_event(
    event_id: int,
    db: Session = Depends(get_db),

    admin = Depends(get_current_admin)
):

    return EventService.delete_event(
        db,
        event_id
    )