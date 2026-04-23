from sqlalchemy import Column, Integer, String
from app.db.base import Base   # make sure this works (we fix below)

class BoardMember(Base):
    __tablename__ = "board_members"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    professional_title = Column(String)
    current_position = Column(String)
    linkedin_url = Column(String)
    twitter_url = Column(String)
    image = Column(String)