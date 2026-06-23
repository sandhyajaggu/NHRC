'''
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from google import genai

from app.core.config import settings
from app.core.database import get_db

from app.models.job import Job
from app.models.job_application import JobApplication

router = APIRouter(
    prefix="/chatbot",
    tags=["AI Chatbot"]
)

# Gemini Client
client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)


class ChatRequest(BaseModel):
    question: str
    membership_id: str | None = None


@router.post("/ask")
def ask_chatbot(
    payload: ChatRequest,
    db: Session = Depends(get_db)
):

    question = payload.question.lower()

    # ==================================
    # 1. HOW MANY JOBS APPLIED
    # ==================================

    if (
    "how many jobs" in question
    and "apply" in question
):

        if not payload.membership_id:

            return {
                "answer": (
                    "Please provide your NHRC Membership ID. "
                    "Example: NHRC-STU-018"
                )
            }

        total = (
            db.query(JobApplication)
            .filter(
                JobApplication.student_membership_id
                == payload.membership_id
            )
            .count()
        )

        return {
            "answer": (
                f"You have applied for {total} jobs."
            )
        }
    # ==================================
    # 2. SHOW MY APPLIED JOBS
    # ==================================

    if (
        "show my applied jobs" in question
        and payload.student_id
    ):

        applications = (
            db.query(JobApplication, Job)
            .join(
                Job,
                Job.id == JobApplication.job_id
            )
            .filter(
                JobApplication.student_id
                == payload.student_id
            )
            .all()
        )

        return {
            "total_applications": len(applications),
            "jobs": [
                {
                    "job_id": job.id,
                    "title": job.title,
                    "company": job.company_name,
                    "status": application.status
                }
                for application, job in applications
            ]
        }

    # ==================================
    # 3. APPLICATION STATUS
    # ==================================

    if (
        "application status" in question
        and payload.student_id
    ):

        applications = (
            db.query(JobApplication)
            .filter(
                JobApplication.student_id
                == payload.student_id
            )
            .all()
        )

        return {
            "applications": [
                {
                    "job_id": app.job_id,
                    "status": app.status
                }
                for app in applications
            ]
        }

    # ==================================
    # 4. GEMINI FALLBACK
    # ==================================

    nhrc_context = """
You are NHRC Website Assistant.

NHRC provides:

1. Student Registration
2. Employee Registration
3. Representative Registration
4. Membership Services
5. Job Portal
6. Job Fair Registration
7. Talent Publications
8. Member Benefits

Student Registration Process:
- Go to Student Registration page
- Fill personal details
- Complete captcha verification
- Submit registration form
- Membership ID will be generated

Employee Registration Process:
- Enter official email
- Verify OTP
- Complete registration form

Representative Registration Process:
- Fill organization details
- Complete registration form

Job Portal:
- Students can apply for jobs
- Students can view applied jobs
- HR can post jobs

Job Fair:
- Students and HR can register
- Admin approves or rejects registrations
- Approved users can attend

Rules:
- Answer NHRC-related questions only.
- If unrelated, respond:
'I can only assist with NHRC services.'
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""
{nhrc_context}

User Question:
{payload.question}
"""
    )

    return {
        "answer": response.text
    }'''