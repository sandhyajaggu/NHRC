from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.otp import OTPRequest, OTPVerifyRequest
from app.services.otp_service import OTPService
from app.utils.email_sender import EmailService

router = APIRouter(prefix="/otp", tags=["OTP"])


@router.post("/send-otp")
def send_otp(email: str):
    EmailService.send_otp(email)
    return {"message": "OTP sent successfully"}

@router.post("/otp/verify")
def verify_otp(payload: dict):
    email = payload.get("email")
    otp = payload.get("otp")

    if not email or not otp:
        raise HTTPException(400, "email and otp required")

    is_valid, message = verify_otp(email, otp)

    if not is_valid:
        raise HTTPException(400, detail=message)

    return {"message": message}