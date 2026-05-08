from fastapi import HTTPException

from app.models.member import Member

from app.repositories.job_repository import JobRepository
from app.repositories.job_application_repository import JobApplicationRepository


class JobApplicationService:

    @staticmethod
    def apply_job(db, job_id, current_user):

        member = db.query(Member).filter(
            Member.email == current_user.email
        ).first()

        if not member:
            raise HTTPException(404, "Member not found")

        job = JobRepository.get_by_id(db, job_id)

        if not job:
            raise HTTPException(404, "Job not found")

        payload = {
            "job_id": job.id,
            "member_id": member.id
        }

        application = JobApplicationRepository.apply_job(
            db,
            payload
        )

        return {
            "message": "Applied successfully",
            "application_id": application.id
        }

    @staticmethod
    def get_job_applications(db, job_id):

        return JobApplicationRepository.get_job_applications(
            db,
            job_id
        )