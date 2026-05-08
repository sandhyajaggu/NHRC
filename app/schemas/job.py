from pydantic import BaseModel


class JobCreate(BaseModel):

    title: str
    company_name: str

    department: str
    work_mode: str

    description: str
    required_skills: str

    qualification: str

    experience_min: int
    experience_max: int

    salary_min: int
    salary_max: int

    perks: str

    location: str
    locality: str

    openings: int

    application_deadline: str

    whatsapp_number: str

    logo: str