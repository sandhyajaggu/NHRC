
from datetime import datetime
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.board_member import BoardMember
from app.models.event_job_role import EventJobRole
from app.models.event_registration import EventRegistration
from app.models.job import Job
from app.models.job_application import JobApplication
from app.models.job_fair import JobFair
from app.models.member import Member
from app.models.service_event import ServiceEvent
from app.models.training_program import TrainingProgram
from app.models.training_registration import TrainingRegistration
from app.models.user import User
from app.schemas.board_member import BoardMemberResponse
from app.schemas.event_job_role import EventJobRoleCreate
from app.schemas.job import JobCreate, JobUpdate
from app.schemas.jobfair import JobFairCreate
from app.schemas.training import TrainingCreate
from app.schemas.training_registration_create import TrainingRegistrationCreate
from app.services.admin_service import AdminService
from app.schemas.admin import *
from app.schemas.member import MemberStatusUpdate
from app.schemas.member import BulkDeleteRequest
from app.schemas.event import EventCreate

from app.services.download import DownloadService
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

@router.get("/admin/db-check")
def db_check(db: Session = Depends(get_db)):
    database = db.execute(
        text("SELECT current_database()")
    ).scalar()

    return {
        "database": database
    }


@router.get("/admin/table-check")
def table_check(db: Session = Depends(get_db)):
    tables = db.execute(
        text("""
        SELECT tablename
        FROM pg_tables
        WHERE schemaname='public'
        """)
    ).fetchall()

    return [row[0] for row in tables]

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

from sqlalchemy import func, text
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

@router.post("/events/create")
def create_event(
    payload: EventCreate,
    db: Session = Depends(get_db)
):
    event = ServiceEvent(**payload.dict())

    db.add(event)
    db.commit()
    db.refresh(event)

    return event
@router.post("/job-fairs/create")
def create_job_fair(
    payload: JobFairCreate,
    db: Session = Depends(get_db)
):

    job_fair = JobFair(**payload.dict())

    db.add(job_fair)

    db.commit()

    db.refresh(job_fair)

    return job_fair

@router.get("/registrations")
def get_all_registrations(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):

    registrations = db.query(
        EventRegistration
    ).all()

    result = []

    for reg in registrations:

        registration_for = None

        registration_name = None

        if reg.event_id:

            event = db.query(ServiceEvent).filter(
                ServiceEvent.id == reg.event_id
            ).first()

            registration_for = "EVENT"

            registration_name = event.title if event else None

        elif reg.job_fair_id:

            job_fair = db.query(JobFair).filter(
                JobFair.id == reg.job_fair_id
            ).first()

            registration_for = "JOB_FAIR"

            registration_name = (
                job_fair.title
                if job_fair else None
            )

        result.append({

            "registration_id": reg.id,

            "member_id": reg.member_id,

            "member_type": reg.member_type,

            "full_name": reg.full_name,

            "email": reg.email,

            "phone": reg.phone,

            "location": reg.location,

            "registration_type": registration_for,

            "registered_for": registration_name,

            "status": reg.status,

            "created_at": reg.created_at
        })

    return {
        "total_registrations": len(result),
        "registrations": result
    }


@router.post("/job-fairs/{job_fair_id}/roles")
def add_job_role(
    job_fair_id: int,
    payload: EventJobRoleCreate,
    db: Session = Depends(get_db)
):

    role = EventJobRole(
        job_fair_id=job_fair_id,
        company_name=payload.company_name,
        hiring_type=payload.hiring_type,
        job_role=payload.job_role,
        experience=payload.experience,
        openings=payload.openings,
        job_location=payload.job_location,
        salary_min=payload.salary_min,
        salary_max=payload.salary_max,
        education_required=payload.education_required
    )

    db.add(role)

    db.commit()

    db.refresh(role)

    return role


@router.delete("/events/{event_id}")
def delete_event(
    event_id: int,
    db: Session = Depends(get_db)
):

    event = db.query(ServiceEvent).filter(
        ServiceEvent.id == event_id
    ).first()

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    db.delete(event)

    db.commit()

    return {
        "message": "Event deleted successfully"
    }
@router.get("/dashboard")
def registration_dashboard(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):

    total = db.query(
        EventRegistration
    ).count()

    event_count = db.query(
        EventRegistration
    ).filter(
        EventRegistration.event_id != None
    ).count()

    job_fair_count = db.query(
        EventRegistration
    ).filter(
        EventRegistration.job_fair_id != None
    ).count()

    return {

        "total_registrations": total,

        "event_registrations": event_count,

        "job_fair_registrations": job_fair_count
    }
@router.get("/student-registrations")
def get_student_registrations(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):

    registrations = db.query(EventRegistration).filter(
        EventRegistration.member_type == "STUDENT"
    ).all()

    return registrations
@router.get("/admin/hr-registrations")
def get_hr_registrations(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):

    registrations = db.query(
        EventRegistration
    ).filter(
        EventRegistration.member_type == "HR"
    ).all()

    return registrations

@router.get("/event/{event_id}/registrations")
def get_event_registrations(
    event_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):

    registrations = db.query(EventRegistration).filter(
        EventRegistration.event_id == event_id
    ).all()

    return {
        "event_id": event_id,
        "total_registrations": len(registrations),
        "registrations": registrations
    }


@router.get("/job-fair/{job_fair_id}/registrations")
def get_job_fair_registrations(
    job_fair_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):

    registrations = db.query(EventRegistration).filter(
        EventRegistration.job_fair_id == job_fair_id
    ).all()

    return {
        "job_fair_id": job_fair_id,
        "total_registrations": len(registrations),
        "registrations": registrations
    }
@router.get("/events")
def get_all_events(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):

    events = db.query(ServiceEvent).all()

    return {
        "total_events": len(events),
        "events": [
            {
                "id": event.id,
                "title": event.title,
                "program_category": event.program_category,
                "organizer_name": event.organizer_name,
                "event_mode": event.event_mode,
                "start_date": event.start_date,
                "end_date": event.end_date,
                "location": event.location
            }
            for event in events
        ]
    }
@router.get("/job-fairs")
def get_all_job_fairs(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):

    job_fairs = db.query(JobFair).all()

    return {
        "total_job_fairs": len(job_fairs),
        "job_fairs": [
            {
                "id": job_fair.id,
                "title": job_fair.title,
                "organizer_name": job_fair.organizer_name,
                "event_mode": job_fair.event_mode,
                "start_date": job_fair.start_date,
                "end_date": job_fair.end_date,
                "location": job_fair.location
            }
            for job_fair in job_fairs
        ]
    }

@router.post("/training/create")
def create_training(

    payload: TrainingCreate,

    db: Session = Depends(get_db),

    admin=Depends(get_current_admin)
):

    training = TrainingProgram(

        title=payload.title,

        short_description=payload.short_description,

        program_category=payload.program_category,

        training_mode=payload.training_mode,

        trainer_name=payload.trainer_name,

        capacity=payload.capacity,

        contact_email=payload.contact_email,

        banner_image=payload.banner_image,

        start_date=payload.start_date,

        end_date=payload.end_date,

        start_time=payload.start_time,

        end_time=payload.end_time,

        location=payload.location,

        created_by=admin.id,

        created_at=datetime.utcnow(),

        status="OPEN"
    )

    db.add(training)

    db.commit()

    db.refresh(training)

    return {
    "message": "Training Program Created",
    "training": {
        "id": training.id,
        "title": training.title,
        "short_description": training.short_description,
        "program_category": training.program_category,
        "training_mode": training.training_mode,
        "trainer_name": training.trainer_name,
        "capacity": training.capacity,
        "contact_email": training.contact_email,
        "banner_image": training.banner_image,
        "start_date": training.start_date,
        "end_date": training.end_date,
        "start_time": training.start_time,
        "end_time": training.end_time,
        "location": training.location,
        "status": training.status,
        "created_by": training.created_by,
        "created_at": training.created_at
    }
}
@router.get("/training-programs")
def get_training_programs(

    db: Session = Depends(get_db),

    admin=Depends(get_current_admin)
):

    return db.query(
        TrainingProgram
    ).all()
@router.get("/training/{training_id}")
def get_training(

    training_id: int,

    db: Session = Depends(get_db),

    admin=Depends(get_current_admin)
):

    training = db.query(
        TrainingProgram
    ).filter(
        TrainingProgram.id == training_id
    ).first()

    if not training:
        raise HTTPException(
            status_code=404,
            detail="Training Program not found"
        )

    return training
@router.put("/training/{training_id}")
def update_training(

    training_id: int,

    payload: TrainingCreate,

    db: Session = Depends(get_db),

    admin=Depends(get_current_admin)
):

    training = db.query(
        TrainingProgram
    ).filter(
        TrainingProgram.id == training_id
    ).first()

    if not training:
        raise HTTPException(
            status_code=404,
            detail="Training Program not found"
        )

    training.title = payload.title

    training.short_description = payload.short_description

    training.program_category = payload.program_category

    training.training_mode = payload.training_mode

    training.trainer_name = payload.trainer_name

    training.capacity = payload.capacity

    training.contact_email = payload.contact_email

    training.banner_image = payload.banner_image

    training.start_date = payload.start_date

    training.end_date = payload.end_date

    training.start_time = payload.start_time

    training.end_time = payload.end_time

    training.location = payload.location

    db.commit()

    return {
        "message": "Training Program Updated"
    }
@router.delete("/training/{training_id}")
def delete_training(

    training_id: int,

    db: Session = Depends(get_db),

    admin=Depends(get_current_admin)
):

    training = db.query(
        TrainingProgram
    ).filter(
        TrainingProgram.id == training_id
    ).first()

    if not training:
        raise HTTPException(
            status_code=404,
            detail="Training Program not found"
        )

    db.delete(training)

    db.commit()

    return {
        "message": "Training Program Deleted"
    }
@router.get("/training-registrations")
def get_training_registrations(

    db: Session = Depends(get_db),

    admin=Depends(get_current_admin)
):

    return db.query(
        TrainingRegistration
    ).all()
@router.get("/training/student-registrations")
def get_student_training_registrations(

    db: Session = Depends(get_db),

    admin=Depends(get_current_admin)
):

    return db.query(
        TrainingRegistration
    ).filter(
        TrainingRegistration.member_type == "STUDENT"
    ).all()
@router.get("/training/hr-registrations")
def get_hr_training_registrations(

    db: Session = Depends(get_db),

    admin=Depends(get_current_admin)
):

    return db.query(
        TrainingRegistration
    ).filter(
        TrainingRegistration.member_type.in_(
            ["EMPLOYEE", "HR"]
        )
    ).all()
@router.get("/training/{training_id}/registrations")
def get_training_registrations_by_training(

    training_id: int,

    db: Session = Depends(get_db),

    admin=Depends(get_current_admin)
):

    return db.query(
        TrainingRegistration
    ).filter(
        TrainingRegistration.training_id == training_id
    ).all()
@router.get("/training/{training_id}/summary")
def training_summary(

    training_id: int,

    db: Session = Depends(get_db),

    admin=Depends(get_current_admin)
):

    total = db.query(
        TrainingRegistration
    ).filter(
        TrainingRegistration.training_id == training_id
    ).count()

    students = db.query(
        TrainingRegistration
    ).filter(
        TrainingRegistration.training_id == training_id,
        TrainingRegistration.member_type == "STUDENT"
    ).count()

    hr_count = db.query(
        TrainingRegistration
    ).filter(
        TrainingRegistration.training_id == training_id,
        TrainingRegistration.member_type.in_(
            ["EMPLOYEE", "HR"]
        )
    ).count()

    return {
        "training_id": training_id,
        "total_registrations": total,
        "students": students,
        "hr_registrations": hr_count
    }

@router.post(
    "/board-members",
    response_model=BoardMemberResponse
)
def create_board_member(
    payload: BoardMemberCreate,
    db: Session = Depends(get_db)
):
    board_member = BoardMember(
        full_name=payload.full_name,
        professional_title=payload.professional_title,
        current_position=payload.current_position,
        photo_url=payload.photo_url,
        linkedin_url=payload.linkedin_url,
        twitter_url=payload.twitter_url,
        facebook_url=payload.facebook_url
    )

    db.add(board_member)
    db.commit()
    db.refresh(board_member)

    return board_member

@router.get(
    "/board-members",
    response_model=list[BoardMemberResponse]
)
def get_board_members(
    db: Session = Depends(get_db)
):
    return db.query(BoardMember)\
        .order_by(BoardMember.id.desc())\
        .all()
@router.get(
    "/board-members/{member_id}",
    response_model=BoardMemberResponse
)
def get_board_member(
    member_id: int,
    db: Session = Depends(get_db)
):
    member = db.query(BoardMember)\
        .filter(BoardMember.id == member_id)\
        .first()

    if not member:
        raise HTTPException(
            status_code=404,
            detail="Board Member not found"
        )

    return member

@router.put(
    "/board-members/{member_id}",
    response_model=BoardMemberResponse
)
def update_board_member(
    member_id: int,
    payload: BoardMemberCreate,
    db: Session = Depends(get_db)
):
    member = db.query(BoardMember)\
        .filter(BoardMember.id == member_id)\
        .first()

    if not member:
        raise HTTPException(
            status_code=404,
            detail="Board Member not found"
        )

    member.full_name = payload.full_name
    member.professional_title = payload.professional_title
    member.current_position = payload.current_position

    member.photo_url = payload.photo_url

    member.linkedin_url = payload.linkedin_url
    member.twitter_url = payload.twitter_url
    member.facebook_url = payload.facebook_url

    db.commit()
    db.refresh(member)

    return member

@router.delete("/board-members/{member_id}")
def delete_board_member(
    member_id: int,
    db: Session = Depends(get_db)
):
    member = db.query(BoardMember)\
        .filter(BoardMember.id == member_id)\
        .first()

    if not member:
        raise HTTPException(
            status_code=404,
            detail="Board Member not found"
        )

    db.delete(member)
    db.commit()

    return {
        "message": "Board Member deleted successfully"
    }