from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.member import Member
from app.models.job import Job

from app.repositories.job_repository import JobRepository
from app.repositories.job_application_repository import (
    JobApplicationRepository
)


class JobService:

    @staticmethod
    def create_admin_job(db: Session, payload):

        data = payload.dict()

        data["posted_by_role"] = "admin"
        data["status"] = "approved"

        return JobRepository.create(db, data)

    @staticmethod
    def create_hr_job(db: Session, payload):

        data = payload.dict()

        data["posted_by_role"] = "hr"

        # IMPORTANT
        data["status"] = "pending"

        return JobRepository.create(
            db,
            data
        )

    @staticmethod
    def get_all_jobs(db: Session):

        return JobRepository.get_all_approved_jobs(db)

    @staticmethod
    def get_pending_jobs(db: Session):

        return JobRepository.get_pending_jobs(db)

    @staticmethod
    def approve_job(
        db: Session,
        job_id: int
    ):

        job = JobRepository.get_job_by_id(
            db,
            job_id
        )

        if not job:
            raise HTTPException(
                404,
                "Job not found"
            )

        return JobRepository.approve_job(
            db,
            job
        )

    @staticmethod
    def reject_job(
        db: Session,
        job_id: int
    ):

        job = JobRepository.get_job_by_id(
            db,
            job_id
        )

        if not job:
            raise HTTPException(
                404,
                "Job not found"
            )

        return JobRepository.reject_job(
            db,
            job
        )

    @staticmethod
    def apply_job(db: Session, payload):

        job = JobRepository.get_job_by_id(
            db,
            payload.job_id
        )

        if not job:
            raise HTTPException(
                404,
                "Job not found"
            )

        if job.status != "approved":
            raise HTTPException(
                400,
                "Job not approved"
            )

        student = db.query(Member).filter(
            Member.membership_id == payload.membership_id
        ).first()

        if not student:
            raise HTTPException(
                404,
                "Student not found"
            )

        data = {
            "job_id": payload.job_id,
            "membership_id": payload.membership_id
        }

        return JobApplicationRepository.create(
            db,
            data
        )

    @staticmethod
    def get_job_details(
        db: Session,
        job_id: int
    ):

        job = JobRepository.get_job_by_id(
            db,
            job_id
        )

        if not job:
            raise HTTPException(
                404,
                "Job not found"
            )

        return job

    @staticmethod
    def get_employee_jobs(
        db: Session,
        membership_id: str
    ):

        return JobRepository.get_employee_jobs(
            db,
            membership_id
        )
    
    @staticmethod
    def delete_job(
        db: Session,
        job_id: int
    ):

        job = JobRepository.get_job_by_id(
            db,
            job_id
        )

        if not job:
            raise HTTPException(
                404,
                "Job not found"
            )

        JobRepository.delete_job(
            db,
            job
        )

        return {
            "message": "Job deleted successfully"
        }
    
    @staticmethod
    def update_job(
        db: Session,
        job_id: int,
        payload
    ):

        job = JobRepository.get_job_by_id(
            db,
            job_id
        )

        if not job:
            raise HTTPException(
                404,
                "Job not found"
            )

        return JobRepository.update_job(
            db,
            job,
            payload.dict()
        )