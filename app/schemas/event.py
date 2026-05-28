from pydantic import BaseModel
from datetime import date, time


class EventCreate(BaseModel):

    service_id: int

    title: str

    description: str

    program_category: str

    speaker_name: str | None = None

    organizer_name: str

    event_mode: str

    start_date: date

    end_date: date

    start_time: time

    end_time: time

    location: str