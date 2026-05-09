from sqlalchemy.orm import Session
from app.models.job import Job


class JobRepository:

    @staticmethod
    def create(db: Session, payload):

        job = Job(**payload)

        db.add(job)
        db.commit()
        db.refresh(job)

        return job

    @staticmethod
    def get_all_approved_jobs(db: Session):

        return db.query(Job).filter(
            Job.status == "approved"
        ).all()

    @staticmethod
    def get_pending_jobs(db: Session):

        return db.query(Job).filter(
            Job.status == "pending"
        ).all()

    @staticmethod
    def get_job_by_id(db: Session, job_id: int):

        return db.query(Job).filter(
            Job.id == job_id
        ).first()

    @staticmethod
    def approve_job(db: Session, job):

        job.status = "approved"

        db.commit()
        db.refresh(job)

        return job

    @staticmethod
    def reject_job(db: Session, job):

        job.status = "rejected"

        db.commit()
        db.refresh(job)

        return job

    @staticmethod
    def get_employee_jobs(
        db: Session,
        membership_id: str
    ):

        return db.query(Job).filter(
            Job.membership_id == membership_id
        ).all()
    
    @staticmethod
    def delete_job(db: Session, job):

        db.delete(job)

        db.commit()

        return True
    @staticmethod
    def update_job(db: Session, job, payload):

        for key, value in payload.items():

            setattr(job, key, value)

        db.commit()
        db.refresh(job)

        return job