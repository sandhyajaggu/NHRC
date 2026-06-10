from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)

from app.db.base import Base


class HRJobFairRole(Base):

    __tablename__ = "hr_job_fair_roles"

    id = Column(Integer, primary_key=True)

    registration_id = Column(
        Integer,
        ForeignKey(
            "hr_job_fair_registrations.id"
        ),
        nullable=False
    )

    hiring_type = Column(
        String(100),
        nullable=False
    )

    job_role = Column(
        String(255),
        nullable=False
    )

    experience = Column(
        String(100),
        nullable=False
    )

    no_of_openings = Column(
        Integer,
        nullable=False
    )

    salary_min = Column(
        String(50),
        nullable=False
    )

    salary_max = Column(
        String(50),
        nullable=False
    )

    job_location = Column(
        String(255),
        nullable=False
    )

    education_required = Column(
        String(255),
        nullable=False
    )