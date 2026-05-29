from pydantic import BaseModel

from datetime import date


class JobFairCreate(BaseModel):

    service_id: int

    title: str

    description: str

    organizer_name: str

    event_mode: str

    start_date: date

    end_date: date

    location: str