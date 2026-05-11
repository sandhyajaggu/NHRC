# app/utils/otp_store.py

# simple in-memory store (for testing)
OTP_STORE = {}


def set_otp(email: str, otp: str):
    OTP_STORE[email] = otp


def get_otp(email: str):
    return OTP_STORE.get(email)