from sqlalchemy.orm import Session
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
    def create_member(db, payload):

        # check duplicate
        existing = db.query(Member).filter(Member.email == payload.email).first()
        if existing:
            raise Exception("Member already exists")

        #  generate membership id
        membership_id = generate_membership_id(db, payload.candidate_type)

        #  generate password (INSIDE function)
        raw_password = generate_password()
        hashed_password = hash_password(raw_password)

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
            candidate_type=payload.candidate_type,
            password_hash=hashed_password   
        )

        db.add(member)
        db.commit()
        db.refresh(member)

        return {
            "message": "Member created successfully",
            "membership_id": membership_id,
            "email": payload.email,
            "password": raw_password   
        }