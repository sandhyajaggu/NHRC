from pydantic import BaseModel
from typing import Optional

class JobCreate(BaseModel):
    title: str
    company_name: str
    department: str
    work_mode: str

    roles_responsibilities: str
    required_skills: str

    qualification_required: str

    min_experience: int
    max_experience: int

    min_salary: int
    max_salary: int

    perks_benefits: str

    location: str
    locality: str

    openings: int

    application_deadline: str

    whatsapp_number: str


class JobUpdate(JobCreate):
    pass