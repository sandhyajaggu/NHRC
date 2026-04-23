import smtplib
from email.mime.text import MIMEText
from app.core.config import settings


class EmailService:

    @staticmethod
    def send_email(to_email: str, subject: str, body: str):

        try:
            msg = MIMEText(body)
            msg["Subject"] = subject
            msg["From"] = settings.EMAIL_USER
            msg["To"] = to_email

            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.starttls()
                server.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
                server.send_message(msg)

            print(" Email sent successfully")

        except Exception as e:
            print(" Email sending failed:", str(e))