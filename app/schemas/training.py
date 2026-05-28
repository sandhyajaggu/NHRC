from datetime import date, time

from pydantic import BaseModel


class CreateTrainingSchema(BaseModel):

    service_id: int

    title: str

    trainer_name: str

    training_mode: str

    start_date: date

    end_date: date

    start_time: time

    end_time: time

    location: str