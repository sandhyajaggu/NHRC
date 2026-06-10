from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey
)
from datetime import datetime

from app.db.base import Base


class StudentJobFairRegistration(Base):

    __tablename__ = "student_job_fair_registrations"

    id = Column(Integer, primary_key=True)

    job_fair_id = Column(
        Integer,
        ForeignKey("job_fairs.id"),
        nullable=False
    )

    full_name = Column(String(255), nullable=False)

    email = Column(String(255), nullable=False)

    phone = Column(String(50), nullable=False)

    location = Column(String(255), nullable=False)

    iam_a = Column(String(100), nullable=False)

    nhrc_id = Column(String(100), nullable=False)

    college_name = Column(String(255), nullable=False)

    year_of_passout = Column(String(50), nullable=False)

    department = Column(String(255), nullable=False)

    preferred_job_role = Column(String(255), nullable=False)

    technical_skills = Column(String, nullable=False)

    receive_updates = Column(
        Boolean,
        default=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )