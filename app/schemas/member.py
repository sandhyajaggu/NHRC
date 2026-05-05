from typing import List

from pydantic import BaseModel, EmailStr
from datetime import date
from enum import Enum


class MemberCreate(BaseModel):
    full_name: str
    gender: str
    dob: date
    state: str
    district: str
    pincode: str
    email: EmailStr
    mobile: str
    blood_group: str
    whatsapp_notification: bool
    candidate_type: str

class StatusEnum(str, Enum):
    approved = "approved"
    rejected = "rejected"


class MemberStatusUpdate(BaseModel):
    status: StatusEnum

class BulkDeleteRequest(BaseModel):
    membership_ids: List[str]