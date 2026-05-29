from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Time,
    DateTime,
    ForeignKey
)

from app.core.database import Base


class ServiceEvent(Base):

    __tablename__ = "service_events"

    id = Column(Integer, primary_key=True, index=True)

    service_id = Column(
        Integer,
        ForeignKey("services.id", ondelete="CASCADE")
    )

    title = Column(String, nullable=False)

    description = Column(String)

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

    status = Column(String)

    created_by = Column(Integer)

    created_at = Column(DateTime)