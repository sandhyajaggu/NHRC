from pydantic import BaseModel,EmailStr


class RepresentativeUniversityCreate(BaseModel):
    member_id: int
    college_name: str
    university_name: str
    college_code: str
    designation: str
    department: str
    state: str
    district: str
    pincode: str
    university_address: str
    experience: int
    official_mail_id: EmailStr
    mobile_number: str


class RepresentativeAutonomousCreate(BaseModel):
    member_id: int
    college_name: str
    college_code: str
    designation: str
    department: str
    state: str
    district: str
    pincode: str
    college_address: str
    experience: int
    official_mail_id: EmailStr
    mobile_number: str



class RepresentativeBothCreate(BaseModel):
    member_id: int
    college_name: str
    university_name: str
    college_code: str
    designation: str
    department: str
    state: str
    district: str
    pincode: str
    university_address: str
    experience: int
    official_mail_id: EmailStr
    mobile_number: str