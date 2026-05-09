from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.member import Member

from app.repositories.job_application_repository import (
    JobApplicationRepository
)


class JobApplicationService:

    @staticmethod
    def get_job_applications(
        db: Session,
        job_id: int
    ):

        applications = JobApplicationRepository.get_job_applications(
            db,
            job_id
        )

        response = []

        for app in applications:

            member = db.query(Member).filter(
                Member.membership_id == app.membership_id
            ).first()

            response.append({
                "application_id": app.id,
                "membership_id": app.membership_id,
                "name": member.full_name if member else None,
                "email": member.email if member else None,
                "mobile": member.mobile if member else None,
                "status": app.application_status
            })

        return response

    @staticmethod
    def shortlist_application(
        db: Session,
        application_id: int
    ):

        app = JobApplicationRepository.get_application_by_id(
            db,
            application_id
        )

        if not app:
            raise HTTPException(
                404,
                "Application not found"
            )

        return JobApplicationRepository.update_status(
            db,
            app,
            "shortlist"
        )

    @staticmethod
    def reject_application(
        db: Session,
        application_id: int
    ):

        app = JobApplicationRepository.get_application_by_id(
            db,
            application_id
        )

        if not app:
            raise HTTPException(
                404,
                "Application not found"
            )

        return JobApplicationRepository.update_status(
            db,
            app,
            "rejected"
        )

    @staticmethod
    def get_student_applications(
        db: Session,
        membership_id: str
    ):

        return JobApplicationRepository.get_student_applications(
            db,
            membership_id
        )