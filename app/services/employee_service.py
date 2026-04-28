from fastapi import HTTPException

from app.models.employee import Employee
from app.core.security import hash_password


class EmployeeService:

    @staticmethod
    def create_employee(db, payload):

        # password match
        if payload.password != payload.confirm_password:
            raise HTTPException(400, "Passwords do not match")

        #  captcha validation (frontend should send correct one)
        if payload.captcha_answer <= 0:
            raise HTTPException(400, "Invalid captcha")

        #  OTP validation (dummy for now)
        if payload.email_otp != "123456":
            raise HTTPException(400, "Invalid OTP")

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
            official_email=payload.official_email,
            email_otp=payload.email_otp,
            user_email=payload.user_email,
            password=hash_password(payload.password)
        )

        db.add(employee)
        db.commit()
        db.refresh(employee)

        return {
            "message": "Employee created successfully",
            "employee_id": employee.id
        }