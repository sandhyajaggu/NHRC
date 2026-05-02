import random
import time

# In-memory store
captcha_store = {}

CAPTCHA_EXPIRY = 300  # 5 minutes


def generate_captcha():
    a = random.randint(1, 9)
    b = random.randint(1, 9)

    captcha_id = str(random.randint(1000, 9999))
    answer = str(a + b)

    captcha_store[captcha_id] = {
        "answer": answer,
        "expiry": int(time.time()) + CAPTCHA_EXPIRY
    }

    return {
        "captcha_id": captcha_id,
        "question": f"{a} + {b} = ?"
    }


def verify_captcha(captcha_id: str, user_answer: str):
    data = captcha_store.get(captcha_id)

    #  Not found
    if not data:
        return False, "Captcha not found"

    #  Expired
    if int(time.time()) > data["expiry"]:
        del captcha_store[captcha_id]
        return False, "Captcha expired"

    #  Wrong answer
    if str(data["answer"]) != str(user_answer):
        return False, "Incorrect captcha"

    #  Success → remove captcha
    del captcha_store[captcha_id]
    return True, "Captcha verified successfully"