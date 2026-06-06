# app/schemas/member_benefit.py

from pydantic import BaseModel
from datetime import datetime


class MemberBenefitCreate(BaseModel):
    category: str
    content: str


class MemberBenefitUpdate(BaseModel):
    content: str


class BenefitStatusUpdate(BaseModel):
    is_active: bool


class MemberBenefitResponse(BaseModel):
    id: int
    category: str
    content: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class BenefitBulkDelete(BaseModel):
    ids: list[int]