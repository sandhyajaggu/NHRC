from enum import member

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.member import MemberCreate
from app.models.member import Member
from app.utils.id_generator import generate_membership_id

router = APIRouter(prefix="/membership", tags=["Membership"])

@router.post("/personal")
def create_member(
    payload: MemberCreate,
    db: Session = Depends(get_db)
):


    db.add(member)
    db.commit()
    db.refresh(member)
    return {
        "message": "Member created successfully",
        "member_id": member.id,
        "membership_id": member.membership_id
    } 