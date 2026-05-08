from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime
)

from datetime import datetime
from app.db.base import Base


class JobApplication(Base):
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, index=True)

    job_id = Column(Integer, ForeignKey("jobs.id"))

    member_id = Column(Integer, ForeignKey("members.id"))

    status = Column(String, default="applied")
    # applied / shortlist / rejected

    applied_at = Column(DateTime, default=datetime.utcnow)