from pydantic import BaseModel
from datetime import date, time
from typing import Optional


class CreateEventSchema(BaseModel):

    service_id: int

    title: str

    description: str

    program_category: str

    speaker_name: Optional[str] = None

    organizer_name: str

    event_mode: str

    start_date: date

    end_date: date

    start_time: time

    end_time: time

    location: str