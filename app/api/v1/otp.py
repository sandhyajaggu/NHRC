from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.otp import OTPRequest, OTPVerifyRequest
from app.services.otp_service import OTPService
from app.utils.email_sender import EmailService
from app.services.otp_service import OTPService


router = APIRouter(prefix="/otp", tags=["OTP"])


@router.post("/send-otp")
def send_otp(email: str):
    EmailService.send_otp(email)
    return {"message": "OTP sent successfully"}


@router.post("/verify")
def verify_otp(payload: OTPVerifyRequest):
    #is_valid, message = verify_otp(payload.email, payload.otp)
    is_valid, message = OTPService.verify_otp(payload.email, payload.otp)

    if not is_valid:
        raise HTTPException(status_code=400, detail=message)

    return {"message": message}