from sqlalchemy import TIMESTAMP, Column, Integer, String, Text, func
from app.db.base import Base

class ContactMessage(Base):
    __tablename__ = "contact_messages"

    id = Column(Integer, primary_key=True, index=True)
    membership_id = Column(String, nullable=False, index=True)
    name = Column(String)
    email = Column(String)
    mobile = Column(String)
    message = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())