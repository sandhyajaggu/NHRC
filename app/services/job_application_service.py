from fastapi import HTTPException

from app.models.member import Member
from app.models.job import Job
from app.repositories.job_application_repository import JobApplicationRepository


class JobApplicationService:

    @staticmethod
    def apply_job(db, job_id, current_user):

        job = db.query(Job).filter(
            Job.id == job_id
        ).first()

        if not job:
            raise HTTPException(
                status_code=404,
                detail="Job not found"
            )

        existing = JobApplicationRepository.get_existing_application(
            db,
            job_id,
            current_user.id
        )

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Already applied"
            )

        return JobApplicationRepository.create_application(
            db,
            job_id,
            current_user.id
        )

    # ✅ ADD THIS METHOD
    @staticmethod
    def get_job_applications(db, job_id):

        job = db.query(Job).filter(
            Job.id == job_id
        ).first()

        if not job:
            raise HTTPException(
                status_code=404,
                detail="Job not found"
            )

        applications = JobApplicationRepository.get_by_job(
            db,
            job_id
        )

        response = []

        for application in applications:

            member = db.query(Member).filter(
                Member.id == application.member_id
            ).first()

            response.append({
                "application_id": application.id,
                "job_id": application.job_id,
                "membership_id": member.membership_id if member else None,
                "name": member.full_name if member else None,
                "email": member.email if member else None,
                "mobile": member.mobile if member else None,
                "status": application.status,
                "applied_at": application.applied_at
            })

        return response