from pydantic import BaseModel

class RegistrationCreate(BaseModel):

    event_id: int | None = None

    job_fair_id: int | None = None