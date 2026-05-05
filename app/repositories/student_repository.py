from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.member import Member
from app.models.student import (
    StudentUniversityDetails,
    StudentAutonomousDetails
)


class StudentRepository:

    @staticmethod
    def create_university(db: Session, payload: dict):
        student = StudentUniversityDetails(**payload)
        db.add(student)
        db.commit()
        db.refresh(student)
        return student

    @staticmethod
    def create_autonomous(db: Session, payload: dict):
        student = StudentAutonomousDetails(**payload)
        db.add(student)
        db.commit()
        db.refresh(student)
        return student

    #  NEW METHOD
    @staticmethod
    def get_students_with_details(db: Session):

        results = db.query(
            Member.membership_id,
            Member.full_name,
            Member.mobile,
            Member.status,

            func.coalesce(
                StudentUniversityDetails.qualification,
                StudentAutonomousDetails.qualification
            ).label("qualification")

        ).outerjoin(
            StudentUniversityDetails,
            StudentUniversityDetails.member_id == Member.id
        ).outerjoin(
            StudentAutonomousDetails,
            StudentAutonomousDetails.member_id == Member.id
        ).filter(
            Member.candidate_type == "student"
        ).all()

        return [
            {
                "membership_id": row.membership_id,
                "name": row.full_name,
                "phone": row.mobile,
                "status": row.status,
                "qualification": row.qualification
            }
            for row in results
        ]