from pydantic import BaseModel, EmailStr, validator


class StudentUniversityCreate(BaseModel):
    member_id: int
    university_name: str
    college_name: str
    college_code: str
    qualification: str
    department: str
    start_year: int
    end_year: int
    location: str
    email: EmailStr
    password: str
    confirm_password: str
    #otp: str
    captcha_answer: int

    @validator("end_year")
    def validate_year(cls, v, values):
        if "start_year" in values and v < values["start_year"]:
            raise ValueError("End year must be greater than start year")
        return v


class StudentAutonomousCreate(BaseModel):
    member_id: int
    college_name: str
    college_code: str
    qualification: str
    department: str
    start_year: int
    end_year: int
    location: str
    email: EmailStr
    password: str
    confirm_password: str
    #otp: str
    captcha_answer: int