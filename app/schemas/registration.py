from pydantic import BaseModel
from typing import Optional


class RegistrationCreate(BaseModel):

    event_id: Optional[int] = None

    job_fair_id: Optional[int] = None

    full_name: str

    phone: str

    location: str

    iam_a: str

    nhrc_id: str

    receive_updates: bool = False

    # STUDENT

    college_name: Optional[str] = None

    year_of_passout: Optional[str] = None

    # HR

    company_name: Optional[str] = None

    company_location: Optional[str] = None