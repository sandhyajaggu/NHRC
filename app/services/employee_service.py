from fastapi import HTTPException
from app.models.employee import Employee
from app.models.otp import OTPVerification
from app.models.member import Member
from app.core.security import hash_password


class EmployeeService:

    @staticmethod
    def create_employee(db, payload):

        # Password validation
        if payload.password != payload.confirm_password:
            raise HTTPException(status_code=400, detail="Passwords do not match")

        #  Captcha validation
        if payload.captcha_answer <= 0:
            raise HTTPException(status_code=400, detail="Invalid captcha")

        #  Get member using membership_id
        member = db.query(Member).filter(
            Member.membership_id == payload.membership_id
        ).first()

        if not member:
            raise HTTPException(status_code=404, detail="Member not found")

        #  OTP check (ONLY verified, not re-validating value)
        otp_record = db.query(OTPVerification).filter(
            OTPVerification.email == payload.official_email
        ).first()

        if not otp_record:
            raise HTTPException(status_code=400, detail="OTP not found")

        if not otp_record.is_verified:
            raise HTTPException(status_code=400, detail="OTP not verified")

        if otp_record.is_used:
            raise HTTPException(status_code=400, detail="OTP already used")

        # (optional) expiry check
        from datetime import datetime
        if datetime.utcnow() > otp_record.expires_at:
            raise HTTPException(status_code=400, detail="OTP expired")

        #  Create employee
        employee = Employee(
            member_id=member.id,
            organization_name=payload.organization_name,
            industry=payload.industry,
            department=payload.department,
            designation=payload.designation,
            company_website=payload.company_website,
            working_location=payload.working_location,
            company_strength=payload.company_strength,
            employee_id=payload.employee_id,
            experience=payload.experience,
            id_card_front=payload.id_card_front,
            id_card_back=payload.id_card_back,
            referral_id=payload.referral_id,
            official_email=payload.official_email,
            user_email=payload.user_email,
            password=hash_password(payload.password)
        )

        db.add(employee)

        #  mark OTP as used AFTER success
        otp_record.is_used = True

        db.commit()
        db.refresh(employee)

        return {
            "message": "Employee created successfully",
            "employee_id": employee.id
        }