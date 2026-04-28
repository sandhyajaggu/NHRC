from sqlalchemy.orm import Session
from app.models.member import Member
from app.schemas.member import MemberCreate
from app.utils.id_generator import generate_membership_id


class MemberService:

    @staticmethod
    def create_member(db: Session, payload: MemberCreate):

        
        existing_member = db.query(Member).filter(Member.email == payload.email).first()
        if existing_member:
            raise Exception("Member already exists with this email")

        
        member = Member(
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
            membership_id=generate_membership_id()  
        )

        db.add(member)   
        db.commit()
        db.refresh(member)

        return member