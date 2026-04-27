from sqlalchemy import Column, Integer, String, Text
from app.core.database import Base


class BlackProfile(Base):
    __tablename__ = "black_profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    designation = Column(String)
    company = Column(String)
    reason = Column(Text)
    status = Column(String, default="active")