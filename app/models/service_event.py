from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Date,
    Time,
    DateTime,
    Text
)

from sqlalchemy.orm import relationship

from datetime import datetime

from app.db.base import Base


class ServiceEvent(Base):
    __tablename__ = "service_events"

    id = Column(Integer, primary_key=True, index=True)

    service_id = Column(
        Integer,
        ForeignKey("services.id", ondelete="CASCADE")
    )

    title = Column(String, nullable=False)

    description = Column(Text)

    program_category = Column(String)

    speaker_name = Column(String)

    organizer_name = Column(String)

    event_mode = Column(String)

    start_date = Column(Date)

    end_date = Column(Date)

    start_time = Column(Time)

    end_time = Column(Time)

    location = Column(String)

    banner_image = Column(String)

    status = Column(String, default="Open")

    created_by = Column(Integer)

    created_at = Column(DateTime, default=datetime.utcnow)

    service = relationship("Service")