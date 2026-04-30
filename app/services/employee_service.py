from fastapi import HTTPException
from app.models.employee import Employee
from app.core.security import hash_password
from app.utils.email_sender import EmailService


class EmployeeService:

    @staticmethod
    def create_employee(db, payload):

        # Password validation
        if payload.password != payload.confirm_password:
            raise HTTPException(status_code=400, detail="Passwords do not match")

        #  Captcha validation
        if payload.captcha_answer <= 0:
            raise HTTPException(status_code=400, detail="Invalid captcha")

        # OTP validation (based on OFFICIAL EMAIL)
        # For now: dummy OTP
        '''if payload.email_otp != "123456":
            raise HTTPException(status_code=400, detail="Invalid OTP")'''
        stored_otp = EmailService.get_otp(payload.official_email)

        if stored_otp != payload.email_otp:
            raise HTTPException(status_code=400, detail="Invalid OTP")

        # Create employee
        employee = Employee(
            member_id=payload.member_id,
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

            #  OTP-related email
            official_email=payload.official_email,
            email_otp=payload.email_otp,

            #  personal login email (no OTP here)
            user_email=payload.user_email,

            #  store hashed password
            password=hash_password(payload.password)
        )

        db.add(employee)
        db.commit()
        db.refresh(employee)

        return {
            "message": "Employee created successfully",
            "employee_id": employee.id
        }