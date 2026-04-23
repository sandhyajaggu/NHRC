from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.member import Member
from app.models.otp import OTPVerification
#from app.models.user import User, UserRole
from app.models.token_blacklist import TokenBlacklist
from app.schemas.auth import RegisterAdminRequest, RegisterRequest, LoginRequest
from app.core.security import hash_password, verify_password, create_access_token
from app.services.otp_service import OTPService
from app.utils.captcha import generate_captcha, verify_captcha
from app.utils.email import generate_otp
from app.utils.id_generator import generate_membership_id
from fastapi import APIRouter, Depends, HTTPException







router = APIRouter(prefix="/auth", tags=["Authentication"])


# ================= ADMIN REGISTER =================
@router.post("/register-admin")
def register_admin(payload: RegisterAdminRequest, db: Session = Depends(get_db)):

    user = db.query(Member).filter(Member.email == payload.email).first()
    if user:
        raise HTTPException(status_code=400, detail="Admin already exists")

    membership_id = generate_membership_id(db, "admin")

    member = Member(
        membership_id=membership_id,
        full_name=payload.full_name,
        email=payload.email,
        password_hash=hash_password(payload.password),  # MUST HASH
        candidate_type="admin",
        role="admin"   
    )

    db.add(member)
    db.commit()
    db.refresh(member)

    print(" ADMIN CREATED:", member.email)

    return {
        "message": "Admin created successfully",
        "membership_id": membership_id
    }
# ================= NORMAL REGISTER =================





@router.post("/register")
def register(payload: RegisterRequest, db: Session = Depends(get_db)):

    # ==============================
    # CHECK EXISTING USER
    # ==============================
    existing = db.query(Member).filter(Member.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    # ==============================
    # PASSWORD VALIDATION
    # ==============================
    if payload.password != payload.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    # ==============================
    # ROLE ASSIGNMENT
    # ==============================
    role = "admin" if payload.candidate_type == "admin" else "user"

    # ==============================
    # EMPLOYEE → OTP VALIDATION
    # ==============================
    if payload.candidate_type == "employee":

        if not payload.otp:
            raise HTTPException(status_code=400, detail="OTP required")

        otp_record = db.query(OTPVerification).filter(
            OTPVerification.email == payload.email
        ).order_by(OTPVerification.id.desc()).first()

        if not otp_record:
            raise HTTPException(status_code=400, detail="OTP not found")

        if otp_record.is_used:
            raise HTTPException(status_code=400, detail="OTP already used")

        if otp_record.expires_at < datetime.utcnow():
            raise HTTPException(status_code=400, detail="OTP expired")

        if otp_record.otp != payload.otp:
            raise HTTPException(status_code=400, detail="Invalid OTP")

        if not otp_record.is_verified:
            raise HTTPException(status_code=400, detail="OTP not verified")

        # mark OTP used
        otp_record.is_used = True
        db.commit()

    # ==============================
    # STUDENT / REPRESENTATIVE → CAPTCHA
    # ==============================
    elif payload.candidate_type in ["student", "representative"]:

        if not payload.captcha or not payload.captcha_id:
            raise HTTPException(status_code=400, detail="Captcha required")

        if not verify_captcha(payload.captcha_id, payload.captcha):
            raise HTTPException(status_code=400, detail="Invalid captcha")

    # ==============================
    # ADMIN → NO VALIDATION REQUIRED
    # ==============================
    elif payload.candidate_type == "admin":
        pass

    else:
        raise HTTPException(status_code=400, detail="Invalid candidate type")

    # ==============================
    # CREATE MEMBER
    # ==============================
    membership_id = generate_membership_id(db, payload.candidate_type)

    member = Member(
        membership_id=membership_id,
        full_name=payload.full_name,
        email=payload.email,
        password_hash=hash_password(payload.password),
        candidate_type=payload.candidate_type,
        role=role
    )

    db.add(member)
    db.commit()
    db.refresh(member)

    return {
        "message": "User registered successfully",
        "membership_id": membership_id,
        "role": role
    }
# ================= LOGIN =================

@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):

    #  fetch user from DB
    user = db.query(Member).filter(Member.email == payload.email).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    #  use INSTANCE (member), not class (Member)
    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.email,"role":user.role})

    return {
        "access_token": token,
        "token_type": "bearer"
    }
# ================= REFRESH =================
@router.post("/refresh")
def refresh_token():
    return {"message": "Implement refresh token logic here"}


@router.get("/captcha")
def get_captcha():
    return generate_captcha()


