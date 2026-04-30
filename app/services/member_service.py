from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.member import Member
from app.schemas.member import MemberCreate
from app.utils.id_generator import generate_membership_id

from app.core.security import hash_password
import random
import string


def generate_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))


class MemberService:

    @staticmethod
    def create_member(db: Session, payload: MemberCreate):

        #  Normalize candidate_type (important for ID generator)
        candidate_type = payload.candidate_type.strip().lower()

        #  Check duplicate email
        existing = db.query(Member).filter(Member.email == payload.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="Member already exists")

        #  Generate membership ID
        membership_id = generate_membership_id(db, candidate_type)

        #  Generate password
        raw_password = generate_password()
        hashed_password = hash_password(raw_password)

        # Create member
        member = Member(
            membership_id=membership_id,
            full_name=payload.full_name,
            gender=payload.gender,
            dob=payload.dob,
            state=payload.state,
            district=payload.district,
            pincode=payload.pincode,
            email=payload.email,
            mobile=payload.mobile,
            blood_group=payload.blood_group,
            whatsapp_notification=payload.whatsapp_notification,
            candidate_type=candidate_type,   
            password_hash=hashed_password
        )

        db.add(member)
        db.commit()
        db.refresh(member)

        return {
            "message": "Member created successfully",
            "membership_id": membership_id,
            "member_id": member.id,   
            "email": payload.email,
            "password": raw_password
        }