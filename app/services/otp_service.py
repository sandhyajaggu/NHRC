import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.models.otp import OTPVerification
from app.utils.email_sender import EmailService
import time
otp_store = {}
OTP_EXPIRY = 300  # 5 minutes

class OTPService:

    @staticmethod
    def generate_and_store_otp(email: str):
        otp = "633822"  # or random
        expiry = int(time.time()) + OTP_EXPIRY

        otp_store[email] = {
            "otp": otp,
            "expiry": expiry
        }

        print(f"OTP for {email}: {otp}")  # debug

        return otp
    @staticmethod
    def verify_otp(email: str, otp: str):
        data = otp_store.get(email)

        if not data:
            return False, "OTP not found"

        if int(time.time()) > data["expiry"]:
            del otp_store[email]
            return False, "OTP expired"

        if str(data["otp"]) != str(otp):
            return False, "Invalid OTP"

        # success → delete OTP
        del otp_store[email]

        return True, "OTP verified"