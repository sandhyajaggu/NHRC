from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime
)
from sqlalchemy.sql import func

from app.core.database import Base


class TalentPublication(Base):
    __tablename__ = "talent_publications"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(255), nullable=False)

    banner_image_1 = Column(String(500), nullable=True)
    banner_image_2 = Column(String(500), nullable=True)
    banner_image_3 = Column(String(500), nullable=True)
    banner_image_4 = Column(String(500), nullable=True)

    document_1 = Column(String(500), nullable=True)
    document_2 = Column(String(500), nullable=True)
    document_3 = Column(String(500), nullable=True)
    document_4 = Column(String(500), nullable=True)

    youtube_url = Column(String(500), nullable=True)

    display_order = Column(Integer, default=1)

    is_active = Column(Boolean, default=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )