from sqlalchemy.orm import Session
from app.models.job_application import JobApplication


class JobApplicationRepository:

    @staticmethod
    def create(db: Session, payload):

        obj = JobApplication(**payload)

        db.add(obj)
        db.commit()
        db.refresh(obj)

        return obj

    @staticmethod
    def get_job_applications(
        db: Session,
        job_id: int
    ):

        return db.query(JobApplication).filter(
            JobApplication.job_id == job_id
        ).all()

    @staticmethod
    def get_application_by_id(
        db: Session,
        application_id: int
    ):

        return db.query(JobApplication).filter(
            JobApplication.id == application_id
        ).first()

    @staticmethod
    def update_status(
        db: Session,
        application,
        status
    ):

        application.application_status = status

        db.commit()
        db.refresh(application)

        return application

    @staticmethod
    def get_student_applications(
        db: Session,
        membership_id: str
    ):

        return db.query(JobApplication).filter(
            JobApplication.membership_id == membership_id
        ).all()