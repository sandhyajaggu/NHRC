from sqlalchemy import Column, Integer, String, Text, DateTime
from app.db.base import Base
from datetime import datetime


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True)

    membership_id = Column(String)

    posted_by_role = Column(String)   # admin / employee

    job_title = Column(String)
    company_name = Column(String)
    department = Column(String)

    work_mode = Column(String)

    roles_responsibilities = Column(Text)

    qualification = Column(String)

    min_experience = Column(Integer)
    max_experience = Column(Integer)

    min_salary = Column(Integer)
    max_salary = Column(Integer)

    perks = Column(Text)

    job_location = Column(String)
    job_locality = Column(String)

    openings = Column(Integer)

    application_deadline = Column(String)

    whatsapp_number = Column(String)

    logo = Column(String)

    status = Column(String, default="pending")

    approved_by = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)