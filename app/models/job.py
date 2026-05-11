from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.sql import func
#from app.core.database import Base
from app.db.base_class import Base
class Job(Base):
    __tablename__ =  "jobs"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)
    company_name = Column(String, nullable=False)
    department = Column(String)
    work_mode = Column(String)

    roles_responsibilities = Column(Text)
    required_skills = Column(Text)

    qualification_required = Column(String)

    min_experience = Column(Integer)
    max_experience = Column(Integer)

    min_salary = Column(Integer)
    max_salary = Column(Integer)

    perks_benefits = Column(Text)

    location = Column(String)
    locality = Column(String)

    openings = Column(Integer)

    application_deadline = Column(String)

    whatsapp_number = Column(String)

    logo = Column(String, nullable=True)

    created_by = Column(String)
    creator_role = Column(String)

    status = Column(String, default="PENDING")
    # PENDING / APPROVED / REJECTED

    is_public = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_by = Column(String, nullable=True)
    updated_at = Column(DateTime(timezone=True), nullable=True)

    deleted_by = Column(String, nullable=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)