from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from datetime import datetime
from app.core.database import Base
import enum

class UserRole(str, enum.Enum):
    admin = "admin"
    employee = "employee"
    student = "student"
    representative = "representative"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String, nullable=False)

    email = Column(String, unique=True, nullable=False)

    mobile = Column(String, unique=True)

    password = Column(String)

    role = Column(Enum(UserRole), nullable=False)

    membership_id = Column(String, unique=True)

    is_active = Column(Boolean, default=True)

    is_approved = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)

