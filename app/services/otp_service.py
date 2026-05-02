# app/services/otp_service.py

import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.otp import OTPVerification


def generate_and_store_otp(db: Session, email: str):
    otp = str(random.randint(100000, 999999))
    expiry = datetime.utcnow() + timedelta(minutes=5)

    #  FIX: handle duplicates safely (instead of .first())
    existing_records = db.query(OTPVerification).filter(
        OTPVerification.email == email
    ).all()

    if existing_records:
        # keep first, delete duplicates
        record = existing_records[0]

        for extra in existing_records[1:]:
            db.delete(extra)

        # update existing
        record.otp = otp
        record.expires_at = expiry
        record.is_verified = False
        record.is_used = False

    else:
        record = OTPVerification(
            email=email,
            otp=otp,
            expires_at=expiry,
            is_verified=False,
            is_used=False
        )
        db.add(record)

    db.commit()

    print(f"OTP for {email}: {otp}")  # debug log

    return otp


def verify_otp(db: Session, email: str, otp: str):
    record = db.query(OTPVerification).filter(
        OTPVerification.email == email
    ).first()

    if not record:
        return False, "OTP not found"

    #  expiry check
    if datetime.utcnow() > record.expires_at:
        return False, "OTP expired"

    #  otp match check
    if record.otp != otp:
        return False, "Invalid OTP"

    #  already used check
    if record.is_used:
        return False, "OTP already used"

    #  mark used
    record.is_verified = True
    record.is_used = True
    db.commit()

    return True, "OTP verified successfully"