from fastapi import HTTPException
from datetime import datetime

from app.models.member import Member

from app.repositories.job_repository import JobRepository


class JobService:

    @staticmethod
    def create_job(db, payload, current_user):

        member = db.query(Member).filter(
            Member.email == current_user.email
        ).first()

        if not member:
            raise HTTPException(404, "Member not found")

        status = "approved" if member.role == "admin" else "pending"

        data = payload.dict()

        data["posted_by"] = member.id
        data["posted_by_type"] = member.role
        data["membership_id"] = member.membership_id
        data["status"] = status

        job = JobRepository.create(db, data)

        return {
            "message": "Job created successfully",
            "job_id": job.id,
            "status": job.status
        }

    @staticmethod
    def get_all_jobs(db):

        return JobRepository.get_all(db)

    @staticmethod
    def get_student_jobs(db):

        return JobRepository.get_approved_jobs(db)

    @staticmethod
    def approve_job(db, job_id: int):

        job = JobRepository.get_by_id(db, job_id)

        if not job:
            raise HTTPException(404, "Job not found")

        # admin jobs already approved
        if job.posted_by_type == "admin":
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
        if job.posted_by_type == "admin":
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