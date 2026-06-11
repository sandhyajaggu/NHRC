# app/schemas/job_fair.py

from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional


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


class JobFairUpdate(BaseModel):
    service_id: Optional[int] = None

    title: Optional[str] = None
    description: Optional[str] = None

    organization_name: Optional[str] = None
    contact_number: Optional[str] = None
    contact_email: Optional[EmailStr] = None

    banner_image: Optional[str] = None

    start_date: Optional[date] = None
    end_date: Optional[date] = None

    start_time: Optional[str] = None
    end_time: Optional[str] = None

    location: Optional[str] = None


from typing import Optional

class JobFairResponse(BaseModel):
    id: int
    service_id: int

    title: str
    description: str

    organization_name: Optional[str] = None
    contact_number: Optional[str] = None
    contact_email: Optional[EmailStr] = None

    banner_image: Optional[str] = None

    start_date: date
    end_date: date

    start_time: Optional[str] = None
    end_time: Optional[str] = None

    location: str

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True