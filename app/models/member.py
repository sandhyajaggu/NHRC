from sqlalchemy import Column, Integer, String, Boolean, Date, TIMESTAMP, func
from app.core.database import Base

class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    membership_id = Column(String(50), unique=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    gender = Column(String(20), nullable=True)
    dob = Column(Date, nullable=True)
    state = Column(String(100), nullable=True)
    district = Column(String(100), nullable=True)
    pincode = Column(String(20), nullable=True)
    email = Column(String(255), unique=True, nullable=False)
    mobile = Column(String(20), nullable=True)
    blood_group = Column(String(10))
    profile_pic = Column(String)
    role = Column(String, default="user")
    whatsapp_notification = Column(Boolean, default=False)
    candidate_type = Column(String(50), nullable=True)
    password_hash = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())