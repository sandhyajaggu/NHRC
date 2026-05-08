from pydantic import BaseModel
from datetime import date


class JobCreate(BaseModel):

    job_title: str
    company_name: str
    department: str

    work_mode: str

    roles_responsibilities: str

    qualification_required: str

    min_experience: int
    max_experience: int

    min_salary: float
    max_salary: float

    perks_benefits: str

    required_skills: str

    job_location: str
    job_locality: str

    openings: int

    application_deadline: date

    whatsapp_number: str

    logo: str