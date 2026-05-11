from pydantic import BaseModel



from typing import Optional, List


class ExperienceSchema(BaseModel):

    previous_company: str

    previous_role: str

    date_of_joining: str

    relieving_date: str

class ApplyJobSchema(BaseModel):

    # =========================
    # PERSONAL INFO
    # =========================

    first_name: str

    last_name: str

    phone_number: str

    email: str

    date_of_birth: str

    gender: str

    location: str

    pan_number: str

    pan_card_file: str

    resume_file: str

    photo_file: str

    linkedin_url: Optional[str] = None

    # =========================
    # EDUCATION
    # =========================

    highest_qualification: str

    specialization: str

    university: str

    college: str

    year_of_passing: str

    # =========================
    # JOB DETAILS
    # =========================

    position_applied_for: str

    preferred_work_mode: str

    key_skills: str

    expected_salary: str

    why_hire_me: str

    # =========================
    # EXPERIENCE
    # =========================

    experience_type: str
    # FRESHER / EXPERIENCED

    experiences: Optional[
        List[ExperienceSchema]
    ] = []