from sqlalchemy import Column, Integer, String, Text
from app.core.database import Base


class ContactMessage(Base):
    __tablename__ = "contact_messages"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)
    email = Column(String)
    mobile = Column(String)
    message = Column(Text)