from pydantic import BaseModel, EmailStr
from datetime import date, time

class TrainingCreate(BaseModel):

    title: str

    short_description: str

    training_mode: str

    program_category: str

    capacity: int

    trainer_name: str

    contact_email: EmailStr

    start_date: date

    end_date: date

    start_time: time

    end_time: time

    location: str

    banner_image: str