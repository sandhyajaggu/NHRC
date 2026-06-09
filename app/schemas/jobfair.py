# app/schemas/job_fair.py

from pydantic import BaseModel, EmailStr
from datetime import date, datetime


class JobFairCreate(BaseModel):
    service_id: int

    title: str
    description: str

    organization_name: str

    contact_number: str
    contact_email: EmailStr

    banner_image: str

    start_date: date
    end_date: date

    start_time: str
    end_time: str

    location: str

class JobFairResponse(BaseModel):
    id: int
    service_id: int

    title: str
    description: str

    organization_name: str
    contact_number: str
    contact_email: EmailStr

    banner_image: str

    start_date: date
    end_date: date

    start_time: str
    end_time: str

    location: str

    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True