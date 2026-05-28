from pydantic import BaseModel
from datetime import date, time



class CreateJobFairSchema(BaseModel):

    title: str

    organization_name: str

    date: date

    start_time: time

    end_time: time

    location: str