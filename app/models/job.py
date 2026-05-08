from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Text,
    Date,
    DateTime,
    ForeignKey
)

from datetime import datetime
from app.db.base import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)

    posted_by = Column(Integer, ForeignKey("members.id"))

    posted_by_type = Column(String)
    # admin / employee

    membership_id = Column(String)

    job_title = Column(String)
    company_name = Column(String)
    department = Column(String)

    work_mode = Column(String)

    roles_responsibilities = Column(Text)

    qualification_required = Column(String)

    min_experience = Column(Integer)
    max_experience = Column(Integer)

    min_salary = Column(Float)
    max_salary = Column(Float)

    perks_benefits = Column(Text)

    required_skills = Column(Text)

    job_location = Column(String)
    job_locality = Column(String)

    openings = Column(Integer)

    application_deadline = Column(Date)

    whatsapp_number = Column(String)

    logo = Column(String)

    status = Column(String, default="pending")
    # pending / approved / rejected

    created_at = Column(DateTime, default=datetime.utcnow)

    approved_at = Column(DateTime, nullable=True)

    approved_by = Column(Integer, nullable=True)