from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.database import Base


class StudentUniversityDetails(Base):
    __tablename__ = "student_university_details"

    id = Column(Integer, primary_key=True, index=True)

    member_id = Column(
        Integer,
        ForeignKey("members.id", ondelete="CASCADE")
    )

    university_name = Column(String, nullable=False)
    college_name = Column(String, nullable=False)
    college_code = Column(String, nullable=False)

    qualification = Column(String, nullable=False)
    department = Column(String, nullable=False)

    start_year = Column(Integer, nullable=False)
    end_year = Column(Integer, nullable=False)

    location = Column(String, nullable=False)

    # 🔐 login fields
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)

    # 📂 file uploads
    id_front = Column(String)
    id_back = Column(String)

class StudentAutonomousDetails(Base):
    __tablename__ = "student_autonomous_details"

    id = Column(Integer, primary_key=True, index=True)

    member_id = Column(
        Integer,
        ForeignKey("members.id", ondelete="CASCADE")
    )

    college_name = Column(String, nullable=False)
    college_code = Column(String, nullable=False)

    qualification = Column(String, nullable=False)
    department = Column(String, nullable=False)

    start_year = Column(Integer, nullable=False)
    end_year = Column(Integer, nullable=False)

    location = Column(String, nullable=False)

    # 🔐 login
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)

    # 📂 uploads
    id_front = Column(String)
    id_back = Column(String)