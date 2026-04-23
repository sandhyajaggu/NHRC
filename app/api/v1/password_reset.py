from fastapi import APIRouter, Depends, HTTPException
from app.core.database import get_db
from app.models.member import Member
from sqlalchemy.orm import Session

from app.schemas.password_reset import (
    ForgotPasswordRequest,
    ResetPasswordRequest
)
from app.utils.email_sender import EmailService

router = APIRouter(
    prefix="/password",
    tags=["Password Reset"]
)


@router.post("/forgot-password")
def forgot_password(email: str, db: Session = Depends(get_db)):

    user = db.query(Member).filter(Member.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    reset_token = "123456"  # or generate JWT/token

    EmailService.send_email(
        to_email=email,
        subject="Password Reset",
        body=f"Your reset code is: {reset_token}"
    )

    return {"message": "Reset email sent"}


@router.post("/reset-password")
def reset_password(payload: ResetPasswordRequest):
    return {"message": "Password updated"}