from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey
)

from app.db.base import Base


class EventRegistration(Base):

    __tablename__ = "event_registrations"

    id = Column(Integer, primary_key=True, index=True)

    member_id = Column(
        Integer,
        ForeignKey("members.id")
    )

    event_id = Column(
        Integer,
        ForeignKey("service_events.id")
    )

    member_type = Column(String)

    full_name = Column(String)

    email = Column(String)

    phone = Column(String)

    location = Column(String)

    nhrc_id = Column(String)

    college_name = Column(String)

    year_of_passout = Column(String)

    company_name = Column(String)

    company_location = Column(String)

    company_url = Column(String)

    resume = Column(String)

    status = Column(String)

    forwarded_to = Column(String)

    approved_by = Column(Integer)

    approved_at = Column(DateTime)

    created_at = Column(DateTime)