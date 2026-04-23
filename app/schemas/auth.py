from pydantic import BaseModel, EmailStr, Field
from typing import Optional


# ================= ADMIN =================
class RegisterAdminRequest(BaseModel):
    full_name: str
    email: EmailStr
    password: str = Field(min_length=6, max_length=72)


# ================= USER REGISTER =================
class RegisterRequest(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    confirm_password: str
    candidate_type: str

    otp: Optional[str] = None
    captcha: Optional[str] = None
    captcha_id: Optional[str] = None


# ================= LOGIN =================
class LoginRequest(BaseModel):
    email: EmailStr
    password: str