from sqlalchemy.orm import Session
from app.models.job_application import JobApplication


class JobApplicationRepository:

    @staticmethod
    def apply_job(db: Session, payload):

        application = JobApplication(**payload)

        db.add(application)

        db.commit()

        db.refresh(application)

        return application

    @staticmethod
    def get_job_applications(db: Session, job_id: int):

        return db.query(JobApplication).filter(
            JobApplication.job_id == job_id
        ).all()

    @staticmethod
    def get_application_by_id(db: Session, application_id: int):

        return db.query(JobApplication).filter(
            JobApplication.id == application_id
        ).first()