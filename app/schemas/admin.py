from pydantic import BaseModel


# ---------------- BOARD MEMBER ----------------

class BoardMemberCreate(BaseModel):
    full_name: str
    professional_title: str
    current_position: str
    linkedin_url: str | None = None
    twitter_url: str | None = None
    image: str | None = None


# ---------------- BENEFITS ----------------

class BenefitCreate(BaseModel):
    role: str  # employee / student / representative
    title: str


# ---------------- BLACK PROFILE ----------------

class BlackProfileCreate(BaseModel):
    name: str
    designation: str
    company: str
    reason: str