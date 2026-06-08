from pydantic import BaseModel
from typing import Optional


class TalentPublicationCreate(BaseModel):
    title: str
    cover_image: str
    pdf_file: str
    display_order: int = 1


class TalentPublicationUpdate(BaseModel):
    title: Optional[str] = None
    cover_image: Optional[str] = None
    pdf_file: Optional[str] = None
    display_order: Optional[int] = None
    is_active: Optional[bool] = None


class TalentPublicationConfigSchema(BaseModel):
    youtube_url: Optional[str] = None