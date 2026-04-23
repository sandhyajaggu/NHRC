import random
import time

def generate_otp():
    otp = str(random.randint(100000, 999999))
    expiry = int(time.time()) + 300  # 5 minutes
    return otp, expiry