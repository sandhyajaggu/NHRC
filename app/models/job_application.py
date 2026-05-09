from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from app.db.base import Base
from datetime import datetime


class JobApplication(Base):
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True)

    job_id = Column(Integer, ForeignKey("jobs.id"))

    membership_id = Column(String)

    application_status = Column(
        String,
        default="applied"
    )

    created_at = Column(DateTime, default=datetime.utcnow)