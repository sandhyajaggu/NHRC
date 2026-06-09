from app.core.database import Base
from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime

class TalentPublication(Base):
    __tablename__ = "talent_publications"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(255), nullable=False)

    banner_image_1 = Column(Text)
    banner_image_2 = Column(Text)
    banner_image_3 = Column(Text)
    banner_image_4 = Column(Text)

    document_1 = Column(Text)
    document_2 = Column(Text)
    document_3 = Column(Text)
    document_4 = Column(Text)

    youtube_url = Column(Text)

    display_order = Column(Integer, default=1)

    created_at = Column(DateTime, default=datetime.utcnow)