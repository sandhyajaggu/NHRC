from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime

from app.db.base import Base


class Job(Base):

    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)

    # basic
    title = Column(String)
    company_name = Column(String)

    department = Column(String)
    work_mode = Column(String)

    description = Column(Text)
    required_skills = Column(Text)

    qualification = Column(String)

    experience_min = Column(Integer)
    experience_max = Column(Integer)

    salary_min = Column(Integer)
    salary_max = Column(Integer)

    perks = Column(Text)

    location = Column(String)
    locality = Column(String)

    openings = Column(Integer)

    application_deadline = Column(String)

    whatsapp_number = Column(String)

    logo = Column(String)

    # job workflow
    status = Column(String, default="pending")

    created_by = Column(Integer)
    created_by_role = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)

    approved_at = Column(DateTime, nullable=True)

    rejected_at = Column(DateTime, nullable=True)