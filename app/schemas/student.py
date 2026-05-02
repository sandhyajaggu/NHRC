from enum import member

from pydantic import BaseModel, EmailStr, validator


from pydantic import BaseModel

class StudentUniversityCreate(BaseModel):
    membership_id: str
    university_name: str
    college_name: str
    college_code: str
    qualification: str
    department: str
    start_year: int
    end_year: int
    location: str
    email: str
    captcha_answer: int

    @validator("end_year")
    def validate_year(cls, v, values):
        if "start_year" in values and v < values["start_year"]:
            raise ValueError("End year must be greater than start year")
        return v


class StudentAutonomousCreate(BaseModel):
    membership_id: str
    university_name: str
    college_name: str
    college_code: str
    qualification: str
    department: str
    start_year: int
    end_year: int
    location: str
    email: str
    captcha_answer: int