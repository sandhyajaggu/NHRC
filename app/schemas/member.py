from pydantic import BaseModel, EmailStr
from datetime import date


class MemberCreate(BaseModel):
    full_name: str
    gender: str
    dob: date
    state: str
    district: str
    pincode: str
    email: EmailStr
    mobile: str
    blood_group: str
    whatsapp_notification: bool
    candidate_type: str