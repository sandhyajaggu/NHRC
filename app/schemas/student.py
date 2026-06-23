from datetime import date
from enum import member
from typing import Optional

from pydantic import BaseModel, EmailStr, validator


from pydantic import BaseModel

class StudentUniversityCreate(BaseModel):
    membership_id: str
    university_name: str
    college_name: str
    college_code: str
    qualification: str
    department: str
    start_year: int
    end_year: int
    location: str
    email: str
    password: str
    confirm_password: str
    captcha_answer: int

    @validator("end_year")
    def validate_year(cls, v, values):
        if "start_year" in values and v < values["start_year"]:
            raise ValueError("End year must be greater than start year")
        return v


class StudentAutonomousCreate(BaseModel):
    membership_id: str
    #university_name: str
    college_name: str
    college_code: str
    qualification: str
    department: str
    start_year: int
    end_year: int
    location: str
    email: str
    password: str
    confirm_password: str
    captcha_answer: int


class StudentProfileUpdate(BaseModel):

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

    # Student Table
    university_name: Optional[str] = None
    college_name: Optional[str] = None
    college_code: Optional[str] = None
    qualification: Optional[str] = None
    department: Optional[str] = None
    start_year: Optional[int] = None
    end_year: Optional[int] = None
    location: Optional[str] = None