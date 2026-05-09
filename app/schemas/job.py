from pydantic import BaseModel
from typing import Optional


class CreateJobRequest(BaseModel):

    membership_id: str

    job_title: str
    company_name: str

    department: Optional[str] = None

    work_mode: Optional[str] = None

    roles_responsibilities: Optional[str] = None

    qualification: Optional[str] = None

    min_experience: Optional[int] = None
    max_experience: Optional[int] = None

    min_salary: Optional[int] = None
    max_salary: Optional[int] = None

    perks: Optional[str] = None

    job_location: Optional[str] = None
    job_locality: Optional[str] = None

    openings: Optional[int] = None

    application_deadline: Optional[str] = None

    whatsapp_number: Optional[str] = None

    logo: Optional[str] = None


class ApplyJobRequest(BaseModel):

    job_id: int
    membership_id: str