from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey
)

from app.db.base import Base


class EventRegistration(Base):

    __tablename__ = "event_registrations"

    id = Column(Integer, primary_key=True)

    member_id = Column(
        Integer,
        ForeignKey("members.id")
    )

    event_id = Column(
        Integer,
        ForeignKey("service_events.id"),
        nullable=True
    )

    job_fair_id = Column(
        Integer,
        ForeignKey("job_fairs.id"),
        nullable=True
    )

    member_type = Column(String)

    full_name = Column(String)

    email = Column(String)

    phone = Column(String)

    location = Column(String)

    iam_a = Column(String)

    nhrc_id = Column(String)

    # STUDENT
    college_name = Column(String)

    year_of_passout = Column(String)

    # HR
    company_name = Column(String)

    company_location = Column(String)

    receive_updates = Column(Boolean)

    status = Column(String)

    created_at = Column(DateTime)