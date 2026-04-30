from pydantic import BaseModel, EmailStr
from typing import Optional
from pydantic import validator
import re


class EmployeeCreate(BaseModel):
    
    membership_id: str
    member_id: int = None

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
    @validator("password")
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError("Password must be at least 6 chars")

        if not re.search(r"[A-Z]", v):
            raise ValueError("Must contain uppercase")

        if not re.search(r"[0-9]", v):
            raise ValueError("Must contain number")

        return v

    captcha_answer: int