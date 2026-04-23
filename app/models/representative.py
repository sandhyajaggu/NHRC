from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.database import Base


class RepresentativeUniversityDetails(Base):
    __tablename__ = "representative_university_details"

    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey("members.id"))

    college_name = Column(String)
    university_name = Column(String)
    college_code = Column(String)
    designation = Column(String)
    department = Column(String)
    state = Column(String)
    district = Column(String)
    pincode = Column(String)
    university_address = Column(String)
    experience = Column(Integer)
    official_mail_id = Column(String)
    mobile_number = Column(String)


class RepresentativeAutonomousDetails(Base):
    __tablename__ = "representative_autonomous_details"

    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey("members.id"))

    college_name = Column(String)
    college_code = Column(String)
    designation = Column(String)
    department = Column(String)
    state = Column(String)
    district = Column(String)
    pincode = Column(String)
    college_address = Column(String)
    experience = Column(Integer)
    official_mail_id = Column(String)
    mobile_number = Column(String)


class RepresentativeBothDetails(Base):
    __tablename__ = "representative_both_details"

    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey("members.id"))

    college_name = Column(String)
    university_name = Column(String)
    college_code = Column(String)
    designation = Column(String)
    department = Column(String)
    state = Column(String)
    district = Column(String)
    pincode = Column(String)

    university_address = Column(String)
    experience = Column(Integer)
    official_mail_id = Column(String)
    mobile_number = Column(String)