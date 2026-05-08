from fastapi import HTTPException
from datetime import datetime

from app.models.job import Job
from app.models.member import Member

from app.repositories.job_repository import JobRepository


class JobService:

    @staticmethod
    def create_job(db, payload, current_user):

        # only admin and employee can post jobs
        if current_user.role not in ["admin", "employee"]:
            raise HTTPException(
                status_code=403,
                detail="Only admin or employee can post jobs"
        )

        # admin jobs auto approved
        status = "approved" if current_user.role == "admin" else "pending"

        job = Job(

            title=payload.title,
            company_name=payload.company_name,

            department=payload.department,
            work_mode=payload.work_mode,

            description=payload.description,
            required_skills=payload.required_skills,

            qualification=payload.qualification,

            experience_min=payload.experience_min,
            experience_max=payload.experience_max,

            salary_min=payload.salary_min,
            salary_max=payload.salary_max,

            perks=payload.perks,

            location=payload.location,
            locality=payload.locality,

            openings=payload.openings,

            application_deadline=payload.application_deadline,

            whatsapp_number=payload.whatsapp_number,

            logo=payload.logo,

            created_by=current_user.id,
            created_by_role=current_user.role,

            status=status
        )

        db.add(job)
        db.commit()
        db.refresh(job)

        return {
            "message": "Job created successfully",
            "job_id": job.id,
            "status": job.status,
            "posted_by_role": job.created_by_role
        }
    @staticmethod
    def get_all_jobs(db):

        jobs = db.query(Job).filter(
            Job.status == "approved"
        ).all()

        response = []

        for job in jobs:

            posted_by = db.query(Member).filter(
                Member.id == job.created_by
            ).first()

            response.append({
                "job_id": job.id,
                "title": job.title,
                "company_name": job.company_name,
                "location": job.location,
                "job_type": job.job_type,
                "department": job.department,
                "work_mode": job.work_mode,
                "required_skills": job.required_skills,
                "qualification": job.qualification,
                "experience_min": job.experience_min,
                "experience_max": job.experience_max,
                "salary_min": job.salary_min,
                "salary_max": job.salary_max,
                "perks": job.perks,
                "locality": job.locality,
                "openings": job.openings,
                "application_deadline": job.application_deadline,
                "whatsapp_number": job.whatsapp_number,
                "logo": job.logo,
                
                
                "status": job.status,
                "posted_date": job.created_at,

                "posted_by_name": posted_by.full_name if posted_by else None,
                "posted_by_membership_id": posted_by.membership_id if posted_by else None,

                "posted_by_role": job.created_by_role
            })

        return response

    @staticmethod
    def get_student_jobs(db):

        return JobRepository.get_approved_jobs(db)

    @staticmethod
    def approve_job(db, job_id: int):

        job = JobRepository.get_by_id(db, job_id)

        if not job:
            raise HTTPException(404, "Job not found")

        # admin jobs already approved
        if job.created_by_role == "admin":
            raise HTTPException(
                status_code=400,
                detail="Admin jobs do not require approval"
            )

        if job.status == "approved":
            raise HTTPException(
                status_code=400,
                detail="Job already approved"
            )

        job.approved_at = datetime.utcnow()

        return JobRepository.approve_job(db, job)
    @staticmethod
    def reject_job(db, job_id: int):

        job = JobRepository.get_by_id(db, job_id)

        if not job:
            raise HTTPException(404, "Job not found")

        # admin jobs cannot be rejected
        if job.created_by_role == "admin":
            raise HTTPException(
                status_code=400,
                detail="Admin jobs cannot be rejected"
            )

        if job.status == "rejected":
            raise HTTPException(
                status_code=400,
                detail="Job already rejected"
            )

        return JobRepository.reject_job(db, job)
    @staticmethod
    def get_job_by_id(db, job_id: int):

        job = JobRepository.get_by_id(db, job_id)

        if not job:
            raise HTTPException(404, "Job not found")

        return job
    
    @staticmethod
    def delete_job(db, job_id: int):

        job = JobRepository.get_by_id(db, job_id)

        if not job:
            raise HTTPException(
                status_code=404,
                detail="Job not found"
            )

        JobRepository.delete_job(db, job)

        return {
            "message": "Job deleted successfully",
            "job_id": job_id
        }


    