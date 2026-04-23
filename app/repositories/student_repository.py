from sqlalchemy.orm import Session
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