from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.board_member import BoardMember
from app.models.member import Member
from app.services.admin_service import AdminService
from app.services.admin_service import AdminExtraService
from app.schemas.admin import *

from app.core.dependencies import get_current_admin  # ✅ IMPORTANT

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

# ================= DASHBOARD =================
@router.get("/dashboard")
def dashboard(
    db: Session = Depends(get_db),
    admin: Member = Depends(get_current_admin)
):
    return AdminService.dashboard_stats(db)


# ================= USERS =================
@router.get("/employees")
def get_employees(
    db: Session = Depends(get_db),
    admin: Member = Depends(get_current_admin)
):
    return AdminService.list_users(db, "employee")


@router.get("/students")
def get_students(
    db: Session = Depends(get_db),
    admin: Member = Depends(get_current_admin)   # ✅ FIXED
):
    return AdminService.list_users(db, "student")


@router.get("/representatives")
def get_representatives(
    db: Session = Depends(get_db),
    admin: Member = Depends(get_current_admin)   # ✅ FIXED
):
    return AdminService.list_users(db, "representative")


# ================= APPROVAL =================
@router.post("/approve/{user_id}")
def approve_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: Member = Depends(get_current_admin)
):
    return AdminService.approve_user(db, user_id)


@router.put("/reject/{user_id}")
def reject_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: Member = Depends(get_current_admin)   # ✅ FIXED
):
    return AdminService.reject_user(db, user_id)


# ================= DELETE MEMBER =================
@router.delete("/member/{member_id}")
def delete_member(
    member_id: int,
    db: Session = Depends(get_db),
    admin: Member = Depends(get_current_admin)   # ✅ FIXED
):
    member = db.query(Member).filter(Member.id == member_id).first()

    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    try:
        db.delete(member)
        db.commit()
        return {"message": "Member deleted successfully"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# ================= EXTRA ADMIN FEATURES =================
import os

UPLOAD_DIR = "uploads/board_members"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/board-members/upload")
def create_board_member_with_image(
    full_name: str,
    professional_title: str = None,
    current_position: str = None,
    linkedin_url: str = None,
    twitter_url: str = None,
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin)
):
    file_path = f"{UPLOAD_DIR}/{image.filename}"

    with open(file_path, "wb") as f:
        f.write(image.file.read())

    new_member = BoardMember(
        full_name=full_name,
        professional_title=professional_title,
        current_position=current_position,
        linkedin_url=linkedin_url,
        twitter_url=twitter_url,
        image=file_path
    )

    db.add(new_member)
    db.commit()
    db.refresh(new_member)

    return {
        "message": "Board member created",
        "image": file_path
    }


@router.get("/board-members")
def get_board_members(
    db: Session = Depends(get_db)
):
    members = db.query(BoardMember).all()
    return members


@router.delete("/board-members/{id}")
def delete_member(
    id: int,
    db: Session = Depends(get_db),
    admin: Member = Depends(get_current_admin)
):
    return AdminExtraService.delete_member(db, id)


@router.post("/benefits")
def create_benefit(
    payload: BenefitCreate,
    db: Session = Depends(get_db),
    admin: Member = Depends(get_current_admin)
):
    return AdminExtraService.create_benefit(db, payload)


@router.get("/benefits/{role}")
def get_benefits(
    role: str,
    db: Session = Depends(get_db),
    admin: Member = Depends(get_current_admin)
):
    return AdminExtraService.get_benefits(db, role)


@router.delete("/benefits/{id}")
def delete_benefit(
    id: int,
    db: Session = Depends(get_db),
    admin: Member = Depends(get_current_admin)
):
    return AdminExtraService.delete_benefit(db, id)


@router.post("/black-profile")
def create_black_profile(
    payload: BlackProfileCreate,
    db: Session = Depends(get_db),
    admin: Member = Depends(get_current_admin)
):
    return AdminExtraService.create_black_profile(db, payload)


@router.get("/black-profile")
def list_black_profiles(
    db: Session = Depends(get_db),
    admin: Member = Depends(get_current_admin)
):
    return AdminExtraService.get_black_profiles(db)


@router.delete("/black-profile/{id}")
def delete_black_profile(
    id: int,
    db: Session = Depends(get_db),
    admin: Member = Depends(get_current_admin)
):
    return AdminExtraService.delete_black_profile(db, id)