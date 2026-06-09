from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)

from app.db.base import Base


class EventJobRole(Base):

    __tablename__ = "event_job_roles"

    id = Column(Integer, primary_key=True, index=True)

    job_fair_id = Column(
        Integer,
        ForeignKey("job_fairs.id")
    )

    company_name = Column(String)

    hiring_type = Column(String)

    job_role = Column(String)

    experience = Column(String)

    openings = Column(Integer)

    job_location = Column(String)

    salary_min = Column(String)

    salary_max = Column(String)

    education_required = Column(String)