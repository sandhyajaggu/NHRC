from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime
)
from sqlalchemy.sql import func

from app.db.base import Base


class TalentPublicationConfig(Base):
    __tablename__ = "talent_publication_config"

    id = Column(Integer, primary_key=True)

    banner_1 = Column(String(500))
    banner_2 = Column(String(500))
    banner_3 = Column(String(500))
    banner_4 = Column(String(500))

    document_1 = Column(String(500))
    document_2 = Column(String(500))
    document_3 = Column(String(500))
    document_4 = Column(String(500))

    youtube_url = Column(String(500))

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )