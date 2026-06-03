from sqlalchemy import *
from app.db.base import Base

class TrainingProgram(Base):

    __tablename__ = "training_programs"

    id = Column(Integer, primary_key=True)

    title = Column(String)

    short_description = Column(String)

    program_category = Column(String)

    training_mode = Column(String)

    trainer_name = Column(String)

    capacity = Column(Integer)

    contact_email = Column(String)

    banner_image = Column(String)

    start_date = Column(Date)

    end_date = Column(Date)

    start_time = Column(String)

    end_time = Column(String)

    location = Column(String)

    created_by = Column(Integer)

    created_at = Column(DateTime)

    status = Column(String, default="OPEN")