from sqlalchemy import Column, Integer, String
from app.db.base import Base


class MemberBenefit(Base):
    __tablename__ = "member_benefits"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String)  # employee / student / representative
    title = Column(String)
    is_active = Column(Integer, default=1)