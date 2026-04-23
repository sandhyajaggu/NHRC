import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.models.otp import OTPVerification
from app.utils.email_sender import EmailService


class OTPService:

    @staticmethod
    def generate_and_send_otp(db, email):

        #  delete old OTPs (VERY IMPORTANT)
        db.query(OTPVerification).filter(
            OTPVerification.email == email
        ).delete()

        otp = str(random.randint(100000, 999999))

        record = OTPVerification(
            email=email,
            otp=otp,
            is_verified=False,
            is_used=False,
            expires_at=datetime.utcnow() + timedelta(minutes=5)
        )

        db.add(record)
        db.commit()

        EmailService.send_email(
            to_email=email,
            subject="Your OTP",
            body=f"Your OTP is {otp}"
        )

        return otp

    @staticmethod
    def verify_otp(db, email, otp):

        record = db.query(OTPVerification).filter(
            OTPVerification.email == email
        ).order_by(OTPVerification.id.desc()).first()

        if not record:
            return False

        if record.otp != otp:
            return False

        if record.expires_at < datetime.utcnow():
            return False

        #  ONLY VERIFY
        record.is_verified = True
        db.commit()

        return True