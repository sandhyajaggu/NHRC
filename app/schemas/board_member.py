from pydantic import BaseModel
from typing import Optional

class BoardMemberCreate(BaseModel):
    full_name: str
    professional_title: Optional[str]
    current_position: Optional[str]
    linkedin_url: Optional[str]
    twitter_url: Optional[str]