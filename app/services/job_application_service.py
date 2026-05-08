from fastapi import HTTPException

from app.models.job import Job
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
    def get_member_applications(db, membership_id):

        member = db.query(Member).filter(
            Member.membership_id == membership_id
        ).first()

        if not member:
            raise HTTPException(
                status_code=404,
                detail="Member not found"
            )

        applications = JobApplicationRepository.get_by_member(
            db,
            member.id
        )

        response = []

        for application in applications:

            job = db.query(Job).filter(
                Job.id == application.job_id
            ).first()

            response.append({

                "application_id": application.id,

                "job_id": application.job_id,

                "job_title": job.title if job else None,

                "company_name": job.company_name if job else None,

                "status": application.status,

                "applied_at": application.applied_at
            })

        return response