from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Text,
    Boolean
)

from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import func

from app.core.database import Base


class JobApplication(Base):

    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, index=True)

    job_id = Column(Integer, ForeignKey("jobs.id"))

    student_id = Column(Integer)

    student_membership_id = Column(String)

    # =========================
    # PERSONAL INFO
    # =========================

    first_name = Column(String)
    last_name = Column(String)

    phone_number = Column(String)
    email = Column(String)

    date_of_birth = Column(String)

    gender = Column(String)

    location = Column(String)

    pan_number = Column(String)

    pan_card_file = Column(String)

    resume_file = Column(String)

    photo_file = Column(String)

    linkedin_url = Column(String)

    # =========================
    # EDUCATION
    # =========================

    highest_qualification = Column(String)

    specialization = Column(String)

    university = Column(String)

    college = Column(String)

    year_of_passing = Column(String)

    # =========================
    # JOB DETAILS
    # =========================

    position_applied_for = Column(String)

    preferred_work_mode = Column(String)

    key_skills = Column(Text)

    expected_salary = Column(String)

    why_hire_me = Column(Text)

    # =========================
    # EXPERIENCE
    # =========================

    experience_type = Column(String)
    # FRESHER / EXPERIENCED

    experiences = Column(JSON, nullable=True)

    # =========================
    # STATUS
    # =========================

    status = Column(
        String,
        default="APPLIED"
    )

    applied_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )