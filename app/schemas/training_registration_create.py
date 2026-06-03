from pydantic import BaseModel
from typing import Optional

class TrainingRegistrationCreate(BaseModel):

    training_id: int

    full_name: str

    phone: str

    location: str

    iam_a: str

    nhrc_id: str

    receive_updates: bool

    college_name: Optional[str] = None

    year_of_passout: Optional[str] = None

    company_name: Optional[str] = None

    company_location: Optional[str] = None