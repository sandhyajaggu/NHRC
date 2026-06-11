from datetime import datetime

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


class TalentPublicationUpdate(BaseModel):

    title: Optional[str] = None

    banner_image_1: Optional[str] = None
    banner_image_2: Optional[str] = None
    banner_image_3: Optional[str] = None
    banner_image_4: Optional[str] = None

    document_1: Optional[str] = None
    document_2: Optional[str] = None
    document_3: Optional[str] = None
    document_4: Optional[str] = None

    youtube_url: Optional[str] = None

    display_order: Optional[int] = None

    is_active: Optional[bool] = None


class TalentPublicationResponse(BaseModel):
    id: int

    title: str

    banner_image_1: str | None = None
    banner_image_2: str | None = None
    banner_image_3: str | None = None
    banner_image_4: str | None = None

    document_1: str | None = None
    document_2: str | None = None
    document_3: str | None = None
    document_4: str | None = None

    youtube_url: str | None = None

    display_order: int

    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True
class TalentPublicationConfigSchema(BaseModel):
    youtube_url: Optional[str] = None