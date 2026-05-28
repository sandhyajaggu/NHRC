from pydantic import BaseModel
from datetime import date, time
from typing import Optional


class CreateEventSchema(BaseModel):

    service_id: int

    title: str

    description: Optional[str] = None

    program_category: Optional[str]

    speaker_name: Optional[str]

    organizer_name: Optional[str]

    event_mode: Optional[str]

    start_date: date

    end_date: date

    start_time: time

    end_time: time

    location: str