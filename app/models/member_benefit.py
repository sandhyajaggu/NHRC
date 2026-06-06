# app/models/member_benefit.py

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime
)
from datetime import datetime

from app.db.base import Base


class MemberBenefit(Base):
    __tablename__ = "member_benefits"

    id = Column(Integer, primary_key=True, index=True)

    category = Column(
        String(50),
        nullable=False
    )
    # EMPLOYEE
    # STUDENT
    # TPO

    content = Column(
        String(1000),
        nullable=False
    )

    is_active = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )