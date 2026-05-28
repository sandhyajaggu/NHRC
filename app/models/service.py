from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime

from app.db.base import Base


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False, unique=True)

    slug = Column(String, nullable=False, unique=True)

    description = Column(String)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)