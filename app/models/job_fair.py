# app/models/job_fair.py

from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.sql import func

from app.db.base import Base


class JobFair(Base):
    __tablename__ = "job_fairs"

    id = Column(Integer, primary_key=True, index=True)

    service_id = Column(Integer, nullable=False)

    title = Column(String(255), nullable=False)
    description = Column(String, nullable=False)

    organization_name = Column(String(255), nullable=False)

    contact_number = Column(String(20), nullable=False)
    contact_email = Column(String(255), nullable=False)

    banner_image = Column(String(500), nullable=False)

    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    start_time = Column(String(20), nullable=False)
    end_time = Column(String(20), nullable=False)

    location = Column(String(500), nullable=False)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )