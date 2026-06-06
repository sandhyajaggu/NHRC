from typing import Optional

from pydantic import BaseModel
from datetime import datetime


class BlackProfileCreate(BaseModel):

    employee_name: str
    designation: str
    status: str

    uid_number: str
    employee_id: str
    aadhaar_number: str
    pan_number: str

    email: str
    phone: str
    location: str

    department: str
    mode_of_work: str
    reporting_to: str

    date_of_joining: datetime
    experience: str

    remarks: str

    document_name: str

    hr_name: str
    organisation: str
    hr_department: str

class BlackProfileUpdate(BaseModel):

    employee_name: Optional[str] = None
    designation: Optional[str] = None
    status: Optional[str] = None

    uid_number: Optional[str] = None
    employee_id: Optional[str] = None
    aadhaar_number: Optional[str] = None
    pan_number: Optional[str] = None

    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None

    department: Optional[str] = None
    mode_of_work: Optional[str] = None
    reporting_to: Optional[str] = None

    date_of_joining: Optional[datetime] = None
    experience: Optional[str] = None

    remarks: Optional[str] = None

    document_name: Optional[str] = None
    document_url: Optional[str] = None

    hr_name: Optional[str] = None
    organisation: Optional[str] = None
    hr_department: Optional[str] = None

    photo_url: Optional[str] = None


class BlackProfileResponse(BaseModel):

    id: int

    # Employee Details
    employee_name: str
    designation: str
    photo_url: Optional[str] = None
    status: str

    # Identifiers
    uid_number: str
    employee_id: str
    aadhaar_number: str
    pan_number: str

    # Contact
    email: str
    phone: str
    location: str

    # Employment
    department: str
    mode_of_work: str
    reporting_to: str
    date_of_joining: datetime
    experience: str

    # Remarks
    remarks: Optional[str] = None

    # Documents
    document_name: Optional[str] = None
    document_url: Optional[str] = None

    # HR Details
    hr_name: str
    organisation: str
    hr_department: str

    # Audit Fields
    created_by: Optional[str] = None
    created_by_id: Optional[int] = None
    created_at: datetime

    class Config:
        orm_mode = True