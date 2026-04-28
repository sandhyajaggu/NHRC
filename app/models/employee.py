from sqlalchemy import Column, Integer, String
from app.db.base import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)

    member_id = Column(Integer)

    organization_name = Column(String)
    industry = Column(String)
    department = Column(String)
    designation = Column(String)

    company_website = Column(String)
    working_location = Column(String)
    company_strength = Column(String)

    employee_id = Column(String)
    experience = Column(Integer)

    id_card_front = Column(String)
    id_card_back = Column(String)

    referral_id = Column(String)

    official_email = Column(String)
    email_otp = Column(String)

    user_email = Column(String)
    password = Column(String)