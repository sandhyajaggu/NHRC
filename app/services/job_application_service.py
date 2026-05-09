from datetime import date

from fastapi import HTTPException

from app.models.member import Member
from app.models.job import Job

from app.repositories.job_application_repository import (
    JobApplicationRepository
)


class JobApplicationService:

    @staticmethod
    def apply_job(db, job_id, current_user):

        # only students can apply
        if current_user.role.lower() != "student":
            raise HTTPException(
                status_code=403,
                detail="Only students can apply for jobs"
            )

        # get job
        job = db.query(Job).filter(
            Job.id == job_id
        ).first()

        if not job:
            raise HTTPException(
                status_code=404,
                detail="Job not found"
            )

        # only approved jobs
        if job.status.lower() != "approved":
            raise HTTPException(
                status_code=400,
                detail="Job is not approved yet"
            )

        # inactive / closed job
        if job.is_active is False:
            raise HTTPException(
                status_code=400,
                detail="Job is closed"
            )

        # application deadline check
        if (
            job.application_deadline and
            job.application_deadline < date.today()
        ):
            raise HTTPException(
                status_code=400,
                detail="Application deadline expired"
            )

        # already applied
        existing = JobApplicationRepository.get_existing_application(
            db,
            job_id,
            current_user.id
        )

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Already applied for this job"
            )

        # create application
        application = JobApplicationRepository.create_application(
            db,
            job_id,
            current_user.id
        )

        return {
            "message": "Applied successfully",
            "application_id": application.id,
            "job_id": application.job_id,
            "member_id": current_user.id,
            "membership_id": current_user.membership_id,
            "student_name": current_user.full_name,
            "status": application.status,
            "applied_at": application.applied_at
        }

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

        applications = JobApplicationRepository.get_job_applications(
            db,
            job_id
        )

        response = []

        for application in applications:

            # applicant member
            member = db.query(Member).filter(
                Member.id == application.member_id
            ).first()

            if not member:
                continue

            response.append({
                "application_id": application.id,
                "job_id": application.job_id,

                # student/member details
                "member_id": member.id,
                "membership_id": member.membership_id,
                "name": member.full_name,
                "email": member.email,
                "mobile": member.mobile,
                "gender": member.gender,
                "dob": member.dob,
                "state": member.state,
                "district": member.district,
                "pincode": member.pincode,
 
                # application details
                "application_status": application.status,
                "applied_at": application.applied_at
            })

        return response

    @staticmethod
    def get_application_by_id(db, application_id):

        application = JobApplicationRepository.get_application_by_id(
            db,
            application_id
        )

        if not application:
            raise HTTPException(
                status_code=404,
                detail="Application not found"
            )

        member = db.query(Member).filter(
            Member.id == application.member_id
        ).first()

        return {
            "application_id": application.id,
            "job_id": application.job_id,

            "membership_id":
                member.membership_id if member else None,

            "name":
                member.full_name if member else None,

            "email":
                member.email if member else None,

            "mobile":
                member.mobile if member else None,

            "status": application.status,

            "applied_at": application.applied_at
        }
    
    