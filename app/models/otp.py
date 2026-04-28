from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from app.db.base import Base


class OTPVerification(Base):
    __tablename__ = "otp_verifications"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    otp = Column(String, nullable=False)

    expires_at = Column(DateTime, nullable=False)

    is_verified = Column(Boolean, default=False)
    is_used = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)