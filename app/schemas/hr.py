from pydantic import BaseModel
from typing import Optional


class HRProfileUpdate(BaseModel):
    organization_name: Optional[str] = None
    industry: Optional[str] = None
    department: Optional[str] = None
    designation: Optional[str] = None
    company_website: Optional[str] = None
    working_location: Optional[str] = None
    company_strength: Optional[str] = None
    employee_id: Optional[str] = None
    experience: Optional[str] = None
    user_email: Optional[str] = None