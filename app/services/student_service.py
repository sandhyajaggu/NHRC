from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.student import (
    StudentUniversityDetails,
    StudentAutonomousDetails
)
from app.models.member import Member
from app.services.otp_service import OTPService


class StudentService:

    # 🔹 UNIVERSITY
    @staticmethod
    def create_university(db: Session, payload):

        # 1. Check member
        member = db.query(Member).filter(
            Member.id == payload.member_id
        ).first()

        if not member:
            raise HTTPException(404, "Member not found")

        # 2. Password validation
        if payload.password != payload.confirm_password:
            raise HTTPException(400, "Passwords do not match")

        # 3. OTP validation
        if not OTPService.verify_otp(db, payload.email, payload.otp):
            raise HTTPException(400, "Invalid or expired OTP")

        # 4. CAPTCHA validation (simple)
        if payload.captcha_answer <= 0:
            raise HTTPException(400, "Invalid captcha")

        # 5. Prevent duplicate email
        existing = db.query(StudentUniversityDetails).filter(
            StudentUniversityDetails.email == payload.email
        ).first()

        if existing:
            raise HTTPException(400, "Email already exists")

        # 6. Create record
        student = StudentUniversityDetails(
            member_id=payload.member_id,
            university_name=payload.university_name,
            college_name=payload.college_name,
            college_code=payload.college_code,
            qualification=payload.qualification,
            department=payload.department,
            start_year=payload.start_year,
            end_year=payload.end_year,
            location=payload.location,
            email=payload.email,
            password_hash=hash_password(payload.password)
        )

        db.add(student)
        db.commit()
        db.refresh(student)

        return {"message": "Student university created", "id": student.id}

    # 🔹 AUTONOMOUS
    @staticmethod
    def create_autonomous(db: Session, payload):

        member = db.query(Member).filter(
            Member.id == payload.member_id
        ).first()

        if not member:
            raise HTTPException(404, "Member not found")

        if payload.password != payload.confirm_password:
            raise HTTPException(400, "Passwords do not match")

        if not OTPService.verify_otp(db, payload.email, payload.otp):
            raise HTTPException(400, "Invalid OTP")

        if payload.captcha_answer <= 0:
            raise HTTPException(400, "Invalid captcha")

        existing = db.query(StudentAutonomousDetails).filter(
            StudentAutonomousDetails.email == payload.email
        ).first()

        if existing:
            raise HTTPException(400, "Email already exists")

        student = StudentAutonomousDetails(
            member_id=payload.member_id,
            college_name=payload.college_name,
            college_code=payload.college_code,
            qualification=payload.qualification,
            department=payload.department,
            start_year=payload.start_year,
            end_year=payload.end_year,
            location=payload.location,
            email=payload.email,
            password_hash=hash_password(payload.password)
        )

        db.add(student)
        db.commit()
        db.refresh(student)

        return {"message": "Student autonomous created", "id": student.id}