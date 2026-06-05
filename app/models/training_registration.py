from sqlalchemy import *
from app.db.base import Base

class TrainingRegistration(Base):

    __tablename__ = "training_registrations"

    id = Column(Integer, primary_key=True)

    member_id = Column(
        Integer,
        ForeignKey("members.id")
    )

    training_id = Column(
        Integer,
        ForeignKey("training_programs.id")
    )

    member_type = Column(String)

    full_name = Column(String)

    email = Column(String)

    phone = Column(String)

    location = Column(String)

    iam_a = Column(String)

    nhrc_id = Column(String)

    receive_updates = Column(Boolean)

    # Student Fields

    college_name = Column(String)

    year_of_passout = Column(String)

    # HR Fields

    company_name = Column(String)

    company_location = Column(String)

    #status = Column(String)
    status = Column(
    String,
    nullable=False,
    default="PENDING")

    created_at = Column(DateTime)