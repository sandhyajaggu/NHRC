from datetime import datetime
from unittest.mock import Base

from sqlalchemy import Column, DateTime, Integer, String


class BoardMember(Base):
    __tablename__ = "board_members"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String(255), nullable=False)
    professional_title = Column(String(255), nullable=False)
    current_position = Column(String(255), nullable=False)

    photo_url = Column(String(500), nullable=False)

    linkedin_url = Column(String(500), nullable=False)
    twitter_url = Column(String(500), nullable=False)
    facebook_url = Column(String(500), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)