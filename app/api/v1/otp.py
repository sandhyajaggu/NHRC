from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.otp import OTPVerifyRequest
from app.services.otp_service import generate_and_store_otp, verify_otp

router = APIRouter(prefix="/otp", tags=["OTP"])


#  SEND OTP
@router.post("/send-otp")
def send_otp(email: str, db: Session = Depends(get_db)):
    generate_and_store_otp(db, email)
    return {"message": "OTP sent successfully"}


#  VERIFY OTP
@router.post("/verify")
def verify_otp_api(payload: OTPVerifyRequest, db: Session = Depends(get_db)):
    is_valid, message = verify_otp(db, payload.email, payload.otp)

    if not is_valid:
        raise HTTPException(status_code=400, detail=message)

    return {"message": message}