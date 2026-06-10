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


class HRJobFairRegistration(Base):

    __tablename__ = "hr_job_fair_registrations"

    id = Column(Integer, primary_key=True)

    job_fair_id = Column(
        Integer,
        ForeignKey("job_fairs.id"),
        nullable=False
    )

    company_name = Column(
        String(255),
        nullable=False
    )

    company_url = Column(
        String(500),
        nullable=True
    )

    full_name = Column(
        String(255),
        nullable=False
    )

    nhrc_id = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(255),
        nullable=False
    )

    phone = Column(
        String(50),
        nullable=False
    )

    receive_updates = Column(
        Boolean,
        default=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )