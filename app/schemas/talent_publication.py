from pydantic import BaseModel
from typing import Optional


class TalentPublicationCreate(BaseModel):
    title: str

    banner_image_1: Optional[str] = None
    banner_image_2: Optional[str] = None
    banner_image_3: Optional[str] = None
    banner_image_4: Optional[str] = None

    document_1: Optional[str] = None
    document_2: Optional[str] = None
    document_3: Optional[str] = None
    document_4: Optional[str] = None

    youtube_url: Optional[str] = None

    display_order: int = 1


class TalentPublicationUpdate(TalentPublicationCreate):
    pass

class TalentPublicationConfigSchema(BaseModel):
    youtube_url: Optional[str] = None