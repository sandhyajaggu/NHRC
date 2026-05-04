from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.board_member import BoardMember
from app.models.member import Member
from app.models.user import User
from app.services.admin_service import AdminService
from app.schemas.admin import *
from app.schemas.member import MemberStatusUpdate

from app.core.dependencies import get_current_admin  

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
    admin: Member = Depends(get_current_admin)  
):
    return AdminService.list_users(db, "student")


@router.get("/representatives")
def get_representatives(
    db: Session = Depends(get_db),
    admin: Member = Depends(get_current_admin)   
):
    return AdminService.list_users(db, "representative")


# ================= APPROVAL =================

from sqlalchemy.sql import func
from fastapi import HTTPException

'''@router.put("/members/{membership_id}/status")
def update_member_status(
    membership_id: str,
    payload: MemberStatusUpdate,
    db: Session
):
    member = db.query(Member).filter(
        Member.membership_id == membership_id
    ).first()

    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    #  SET STATUS
    member.status = payload.status

    #  TRACK TIME
    if payload.status == "approved":
        member.approved_at = func.now()
        member.rejected_at = None

    elif payload.status == "rejected":
        member.rejected_at = func.now()
        member.approved_at = None

    db.commit()

    return {
        "message": f"Member {payload.status} successfully",
        "membership_id": membership_id,
        "status": member.status
    }


@router.post("/reject-member/{membership_id}")
def reject_member(membership_id: str, db: Session = Depends(get_db)):

    member = db.query(Member).filter(
        Member.membership_id == membership_id
    ).first()

    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    member.status = "rejected"
    db.commit()

    return {
        "message": "Member rejected successfully",
        "membership_id": member.membership_id
    }

# ================= DELETE MEMBER =================
@router.delete("/delete-member/{membership_id}")
def delete_member(membership_id: str, db: Session = Depends(get_db)):

    member = db.query(Member).filter(
        Member.membership_id == membership_id
    ).first()

    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    db.delete(member)
    db.commit()

    return {
        "message": "Member deleted successfully",
        "membership_id": membership_id
    }'''

@router.put("/members/{membership_id}/approve")
def approve_member(membership_id: str, db: Session = Depends(get_db)):
    return AdminService.approve_user(db, membership_id)


@router.put("/members/{membership_id}/reject")
def reject_member(membership_id: str, db: Session = Depends(get_db)):
    return AdminService.reject_user(db, membership_id)


@router.delete("/members/{membership_id}")
def delete_member(membership_id: str, db: Session = Depends(get_db)):
    return AdminService.delete_user(db, membership_id)

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