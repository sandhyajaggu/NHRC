from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.student import (
    StudentUniversityDetails,
    StudentAutonomousDetails
)
from app.models.member import Member
from app.services.otp_service import OTPService


from fastapi import HTTPException
from app.models.member import Member


class StudentService:

    @staticmethod
    def create_university(db, payload):

        # Validate membership_id
        member = db.query(Member).filter(
            Member.membership_id == payload.membership_id
        ).first()

        if not member:
            raise HTTPException(status_code=404, detail="Member not found")

        '''# Password validation
        if payload.password != payload.confirm_password:
            raise HTTPException(status_code=400, detail="Passwords do not match")'''

        # Captcha validation
        if payload.captcha_answer <= 0:
            raise HTTPException(status_code=400, detail="Invalid captcha")

        #  NO OTP VALIDATION FOR STUDENT

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
            #password=payload.password  # (hash if needed)
        )

        db.add(student)
        db.commit()
        db.refresh(student)

        return {
            "message": "Student university details created successfully",
            "student_id": student.id
        }
    # 🔹 AUTONOMOUS
    @staticmethod
    def create_autonomous(db, payload):

        #  Validate membership_id
        member = db.query(Member).filter(
            Member.membership_id == payload.membership_id
        ).first()

        if not member:
            raise HTTPException(status_code=404, detail="Member not found")

        

        #  Captcha validation
        if payload.captcha_answer <= 0:
            raise HTTPException(status_code=400, detail="Invalid captcha")

        #  Create student autonomous record
        student = StudentAutonomousDetails(
            member_id=member.id,
            university_name=payload.university_name,
            college_name=payload.college_name,
            college_code=payload.college_code,
            qualification=payload.qualification,
            department=payload.department,
            start_year=payload.start_year,
            end_year=payload.end_year,
            location=payload.location,
            email=payload.email
        )

        db.add(student)
        db.commit()
        db.refresh(student)

        return {
            "message": "Student autonomous details created successfully",
            "student_id": student.id
        }