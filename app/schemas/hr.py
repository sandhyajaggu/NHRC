from pydantic import BaseModel
from typing import Optional
from datetime import date

class HRProfileUpdate(BaseModel):

    # Member Table
    full_name: Optional[str] = None
    gender: Optional[str] = None
    dob: Optional[date] = None
    state: Optional[str] = None
    district: Optional[str] = None
    pincode: Optional[str] = None
    mobile: Optional[str] = None
    blood_group: Optional[str] = None
    profile_pic: Optional[str] = None
    whatsapp_notification: Optional[bool] = None

    # Employee Table
    organization_name: Optional[str] = None
    industry: Optional[str] = None
    department: Optional[str] = None
    designation: Optional[str] = None
    company_website: Optional[str] = None
    working_location: Optional[str] = None
    company_strength: Optional[str] = None
    employee_id: Optional[str] = None
    experience: Optional[int] = None
    referral_id: Optional[str] = None
    user_email: Optional[str] = None