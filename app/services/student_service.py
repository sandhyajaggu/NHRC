from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.student import (
    StudentUniversityDetails,
    StudentAutonomousDetails
)
from app.models.member import Member


class StudentService:

    # =========================
    # UNIVERSITY STUDENT
    # =========================
    @staticmethod
    def create_university(db, payload):

        # Validate membership_id
        member = db.query(Member).filter(
            Member.membership_id == payload.membership_id
        ).first()

        if not member:
            raise HTTPException(
                status_code=404,
                detail="Member not found"
            )

        # Password validation
        if payload.password != payload.confirm_password:
            raise HTTPException(
                status_code=400,
                detail="Passwords do not match"
            )

        # Captcha validation
        if payload.captcha_answer <= 0:
            raise HTTPException(
                status_code=400,
                detail="Invalid captcha"
            )

        # Store password in MEMBERS table
        member.password_hash = hash_password(payload.password)

        # Optional role/status update
        member.role = "STUDENT"
        member.status = "approved"

        # Create student record
        student = StudentUniversityDetails(
            member_id=member.id,

            university_name=payload.university_name,
            college_name=payload.college_name,
            college_code=payload.college_code,

            qualification=payload.qualification,
            department=payload.department,

            start_year=payload.start_year,
            end_year=payload.end_year,

            location=payload.location,

            email=payload.email,

            # optional
            password_hash=member.password_hash
        )

        db.add(student)

        db.commit()
        db.refresh(student)

        return {
            "message": "Student university details created successfully",
            "student_id": student.id,
            "membership_id": member.membership_id,
            "email": member.email
        }

    # =========================
    # AUTONOMOUS STUDENT
    # =========================
    @staticmethod
    def create_autonomous(db, payload):

        # Validate membership_id
        member = db.query(Member).filter(
            Member.membership_id == payload.membership_id
        ).first()

        if not member:
            raise HTTPException(
                status_code=404,
                detail="Member not found"
            )

        # Password validation
        if payload.password != payload.confirm_password:
            raise HTTPException(
                status_code=400,
                detail="Passwords do not match"
            )

        # Captcha validation
        if payload.captcha_answer <= 0:
            raise HTTPException(
                status_code=400,
                detail="Invalid captcha"
            )

        # Store password in MEMBERS table
        member.password_hash = hash_password(payload.password)

        # Optional role/status update
        member.role = "STUDENT"
        member.status = "approved"

        # Create student record
        student = StudentAutonomousDetails(
            member_id=member.id,

            college_name=payload.college_name,
            college_code=payload.college_code,

            qualification=payload.qualification,
            department=payload.department,

            start_year=payload.start_year,
            end_year=payload.end_year,

            location=payload.location,

            email=payload.email,

            # optional
            password_hash=member.password_hash
        )

        db.add(student)

        db.commit()
        db.refresh(student)

        return {
            "message": "Student autonomous details created successfully",
            "student_id": student.id,
            "membership_id": member.membership_id,
            "email": member.email
        }