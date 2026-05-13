from sqlalchemy import Column, Integer, String
from app.db.base import Base


class UploadedFile(Base):
    __tablename__ = "uploaded_files"

    id = Column(Integer, primary_key=True, index=True)

    membership_id = Column(String)

    file_type = Column(String)

    original_name = Column(String)

    stored_name = Column(String)

    file_path = Column(String)