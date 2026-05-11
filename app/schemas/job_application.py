from pydantic import BaseModel

class ApplyJobSchema(BaseModel):
    resume: str