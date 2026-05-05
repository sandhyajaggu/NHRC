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

@router.get("/member/{membership_id}")
def get_member_full_details(
    membership_id: str,
    db: Session = Depends(get_db),
    admin: Member = Depends(get_current_admin)
):
    return AdminService.get_member_full_details(db, membership_id)

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

@router.delete("/member/{membership_id}")
def delete_member(
    membership_id: str,
    db: Session = Depends(get_db),
    admin: Member = Depends(get_current_admin)
):
    return AdminService.delete_member(db, membership_id)

# ================= EXTRA ADMIN FEATURES =================
