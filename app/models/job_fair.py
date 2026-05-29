from sqlalchemy import (
    Column,
    Integer,
    String,
    Date
)

from app.db.base import Base


class JobFair(Base):

    __tablename__ = "job_fairs"

    id = Column(Integer, primary_key=True, index=True)

    service_id = Column(Integer)

    title = Column(String)

    description = Column(String)

    organizer_name = Column(String)

    event_mode = Column(String)

    start_date = Column(Date)

    end_date = Column(Date)

    location = Column(String)