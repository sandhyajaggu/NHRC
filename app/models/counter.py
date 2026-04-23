from sqlalchemy import Column, Integer, String
from app.core.database import Base

class MembershipCounter(Base):
    __tablename__ = "membership_counters"

    id = Column(Integer, primary_key=True)
    type = Column(String, unique=True)
    current_value = Column(Integer, default=0)