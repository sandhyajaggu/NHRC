captcha_store = {}


def generate_captcha():
    import random

    a = random.randint(1, 9)
    b = random.randint(1, 9)

    captcha_id = str(random.randint(1000, 9999))
    answer = str(a + b)

    captcha_store[captcha_id] = answer

    return {
        "captcha_id": captcha_id,
        "question": f"{a} + {b} = ?"
    }


def verify_captcha(captcha_id: str, user_answer: str):
    correct = captcha_store.get(captcha_id)

    if not correct:
        return False

    return correct == user_answer