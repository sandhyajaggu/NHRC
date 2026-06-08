# app/models/talent_publication.py

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime
)
from sqlalchemy.sql import func

from app.db.base import Base


class TalentPublication(Base):
    __tablename__ = "talent_publications"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(255), nullable=False)

    cover_image = Column(String(500), nullable=False)

    pdf_file = Column(String(500), nullable=False)

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