from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.member import Member
from app.models.student import (
    StudentUniversityDetails,
    StudentAutonomousDetails
)
from fastapi.encoders import jsonable_encoder


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

        university_students = db.query(
            Member,
            StudentUniversityDetails
        ).join(
            StudentUniversityDetails,
            StudentUniversityDetails.member_id == Member.id
        ).filter(
            Member.candidate_type == "student"
        ).all()

        autonomous_students = db.query(
            Member,
            StudentAutonomousDetails
        ).join(
            StudentAutonomousDetails,
            StudentAutonomousDetails.member_id == Member.id
        ).filter(
            Member.candidate_type == "student"
        ).all()

        results = []

        for member, details in university_students:
            results.append({
                "member": member,
                "details": details
            })

        for member, details in autonomous_students:
            results.append({
                "member": member,
                "details": details
            })

        return jsonable_encoder(results)