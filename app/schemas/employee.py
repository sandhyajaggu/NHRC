from pydantic import BaseModel, EmailStr
from typing import Optional


class EmployeeCreate(BaseModel):
    member_id: int

    organization_name: str
    industry: str
    department: str
    designation: str

    company_website: Optional[str]
    working_location: str
    company_strength: str

    employee_id: str
    experience: int

    id_card_front: Optional[str]   # file path
    id_card_back: Optional[str]

    referral_id: Optional[str]

    official_email: EmailStr
    email_otp: Optional[str]

    user_email: EmailStr
    password: str
    confirm_password: str

    captcha_answer: int