from pydantic import BaseModel


class BoardMemberCreate(BaseModel):
    full_name: str
    professional_title: str
    current_position: str

    photo_url: str

    linkedin_url: str
    twitter_url: str
    facebook_url: str


class BoardMemberResponse(BoardMemberCreate):
    id: int

    class Config:
        from_attributes = True