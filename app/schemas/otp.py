from pydantic import BaseModel, EmailStr

class OTPRequest(BaseModel):
    email: str

class OTPVerifyRequest(BaseModel):
    email: EmailStr
    otp: str