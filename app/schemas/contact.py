from datetime import datetime

from pydantic import BaseModel, EmailStr


class ContactCreate(BaseModel):
    name: str
    email: EmailStr
    mobile: str
    message: str

class ContactResponse(BaseModel):
    id: int
    name: str
    email: str
    mobile: str
    message: str
    created_at: datetime

    class Config:
        from_attributes = True