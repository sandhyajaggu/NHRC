from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List


# ==========================================
# STUDENT JOB FAIR REGISTRATION
# ==========================================

class StudentJobFairRegistrationCreate(BaseModel):

    job_fair_id: int

    full_name: str
    email: EmailStr
    phone: str

    location: str

    iam_a: str

    nhrc_id: str

    college_name: str

    year_of_passout: str

    department: str

    preferred_job_role: str

    technical_skills: str

    receive_updates: bool = False


class StudentJobFairRegistrationResponse(
    StudentJobFairRegistrationCreate
):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ==========================================
# HR JOB FAIR ROLE
# ==========================================

class HRRoleCreate(BaseModel):

    hiring_type: str

    job_role: str

    experience: str

    no_of_openings: int

    salary_min: str

    salary_max: str

    job_location: str

    education_required: str


class HRJobRoleResponse(BaseModel):

    id: int

    hiring_type: str

    job_role: str

    experience: str

    no_of_openings: int

    salary_min: str

    salary_max: str

    job_location: str

    education_required: str

    class Config:
        from_attributes = True


# ==========================================
# HR JOB FAIR REGISTRATION
# ==========================================

class HRJobFairRegistrationCreate(BaseModel):

    job_fair_id: int

    company_name: str

    company_url: str

    full_name: str

    nhrc_id: str

    email: EmailStr

    phone: str

    receive_updates: bool = False

    roles: List[HRRoleCreate]


class HRJobFairRegistrationResponse(BaseModel):

    id: int

    job_fair_id: int

    company_name: str

    company_url: str

    full_name: str

    nhrc_id: str

    email: EmailStr

    phone: str

    receive_updates: bool

    created_at: datetime

    class Config:
        from_attributes = True