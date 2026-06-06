from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Text
)
from datetime import datetime

from app.db.base import Base


class BlackProfile(Base):

    __tablename__ = "black_profiles"

    id = Column(Integer, primary_key=True)

    # Employee Details
    employee_name = Column(String(255))
    designation = Column(String(255))
    photo_url = Column(String(500))
    status = Column(String(50))

    # Identifiers
    uid_number = Column(String(100))
    employee_id = Column(String(100))
    aadhaar_number = Column(String(50))
    pan_number = Column(String(50))

    # Contact
    email = Column(String(255))
    phone = Column(String(50))
    location = Column(String(255))

    # Employment
    department = Column(String(255))
    mode_of_work = Column(String(100))
    reporting_to = Column(String(255))
    date_of_joining = Column(DateTime)
    experience = Column(String(100))

    # Remarks
    remarks = Column(Text)

    # Documents
    document_name = Column(String(255))
    document_url = Column(String(500))

    # HR Details
    hr_name = Column(String(255))
    organisation = Column(String(255))
    hr_department = Column(String(255))

    # Audit
    created_by = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

    created_by_id = Column(Integer)

