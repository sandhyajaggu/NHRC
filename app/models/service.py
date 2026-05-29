from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime
)

from app.core.database import Base


class Service(Base):

    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, unique=True, nullable=False)

    slug = Column(String, unique=True, nullable=False)

    description = Column(String)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime)