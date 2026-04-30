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

@router.post("/verify")
def verify_otp(payload: OTPVerifyRequest, db: Session = Depends(get_db)):
    success = OTPService.verify_otp(db, payload.email, payload.otp)

    if not success:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    return {"message": "OTP verified"}