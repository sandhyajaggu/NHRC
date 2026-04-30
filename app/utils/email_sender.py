import smtplib
import time
import random
from email.mime.text import MIMEText
from app.core.config import settings


#  In-memory OTP store (temporary)
OTP_STORE = {}


class EmailService:

    @staticmethod
    def send_email(to_email: str, subject: str, body: str):
        try:
            msg = MIMEText(body)
            msg["Subject"] = subject
            msg["From"] = settings.EMAIL_USER
            msg["To"] = to_email

            #with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=5) as server:
                server.starttls()
                server.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
                server.send_message(msg)

            print(" Email sent successfully")

        except Exception as e:
            print(" Email sending failed:", str(e))
            return False


    #  Generate + Send OTP
    @staticmethod
    def send_otp(to_email: str):
        otp = str(random.randint(100000, 999999))
        expiry = int(time.time()) + 300  # 5 minutes

        # store OTP
        OTP_STORE[to_email] = {
            "otp": otp,
            "expiry": expiry
        }

        subject = "Your OTP Code"
        body = f"Your OTP is {otp}. It is valid for 5 minutes."

        EmailService.send_email(to_email, subject, body)

        print(f"OTP for {to_email}: {otp}")  # for debugging

        return otp


    #  Get OTP for validation
    @staticmethod
    def get_otp(email: str):
        data = OTP_STORE.get(email)

        if not data:
            return None

        # check expiry
        if int(time.time()) > data["expiry"]:
            del OTP_STORE[email]
            return None

        return data["otp"]