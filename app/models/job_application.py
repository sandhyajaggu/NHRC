from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.db.base_class import Base

class JobApplication(Base):
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, index=True)

    job_id = Column(Integer, ForeignKey("jobs.id"))

    student_id = Column(Integer)
    student_membership_id = Column(String)

    student_name = Column(String)
    email = Column(String)

    qualification = Column(String)
    experience = Column(Integer)

    resume = Column(String)

    status = Column(String, default="APPLIED")
    # APPLIED / SHORTLISTED / REJECTED

    applied_at = Column(DateTime(timezone=True), server_default=func.now())