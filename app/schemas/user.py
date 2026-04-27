from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    mobile: str
    membership_id: str
    role: str
    is_approved: bool

    class Config:
        from_attributes = True