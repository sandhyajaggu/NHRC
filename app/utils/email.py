# app/utils/email.py

import random
import time

#  Temporary in-memory OTP store
OTP_STORE = {}

def generate_otp():
    otp = str(random.randint(100000, 999999))
    expiry = int(time.time()) + 300  # 5 minutes
    return otp, expiry


def set_otp(email: str, otp: str, expiry: int):
    OTP_STORE[email] = {
        "otp": otp,
        "expiry": expiry
    }


def get_otp(email: str):
    data = OTP_STORE.get(email)

    if not data:
        return None

    #  check expiry
    if int(time.time()) > data["expiry"]:
        del OTP_STORE[email]
        return None

    return data["otp"]