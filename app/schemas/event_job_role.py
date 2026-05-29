from pydantic import BaseModel


class EventJobRoleCreate(BaseModel):

    company_name: str

    hiring_type: str

    job_role: str

    experience: str

    openings: int

    job_location: str

    salary_min: str

    salary_max: str

    education_required: str