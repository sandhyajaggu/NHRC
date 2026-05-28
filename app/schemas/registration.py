from pydantic import BaseModel
from typing import Optional


class RegisterEventSchema(BaseModel):

    event_id: int

    member_id: int

    member_type: str

    full_name: str

    email: str

    phone: str

    location: str

    nhrc_id: str

    college_name: Optional[str] = None

    year_of_passout: Optional[str] = None

    company_name: Optional[str] = None

    company_location: Optional[str] = None

    company_url: Optional[str] = None