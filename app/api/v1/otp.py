from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.otp import OTPRequest, OTPVerifyRequest
from app.services.otp_service import OTPService

router = APIRouter(prefix="/otp", tags=["OTP"])


@router.post("/send")
def send_otp(payload: OTPRequest, db: Session = Depends(get_db)):

    OTPService.generate_and_send_otp(db, payload.email)

    return {
        "message": "OTP sent successfully"
    }

@router.post("/verify")
def verify_otp(payload: OTPVerifyRequest, db: Session = Depends(get_db)):
    success = OTPService.verify_otp(db, payload.email, payload.otp)

    if not success:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    return {"message": "OTP verified"}