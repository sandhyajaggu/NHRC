import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.otp import OTPVerification

def generate_and_store_otp(db: Session, email: str):
    otp = str(random.randint(100000, 999999))
    expiry = datetime.utcnow() + timedelta(minutes=5)

    existing = db.query(OTPVerification).filter_by(email=email).first()

    if existing:
        existing.otp = otp
        existing.expires_at = expiry
    else:
        new_otp = OTPVerification(
            email=email,
            otp=otp,
            expires_at=expiry
        )
        db.add(new_otp)

    db.commit()

    print(f"OTP for {email}: {otp}")  # debug
    return otp


def verify_otp(db: Session, email: str, otp: str):
    record = db.query(OTPVerification).filter_by(email=email).first()

    if not record:
        return False, "OTP not found"

    if datetime.utcnow() > record.expires_at:
        return False, "OTP expired"

    if record.otp != otp:
        return False, "Invalid OTP"

    return True, "OTP verified successfully"