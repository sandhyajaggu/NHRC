from sqlalchemy.orm import Session
from app.models.member import Member
from app.schemas.member import MemberCreate
from app.utils.id_generator import generate_membership_id  


class MemberService:

    @staticmethod
    def create_member(db, payload, current_user_email):

        #  GET EXISTING USER (DON'T CREATE NEW)
        member = db.query(Member).filter(Member.email == current_user_email).first()

        if not member:
            raise Exception("User not found")

        #  UPDATE DETAILS
        member.full_name = payload.full_name
        member.gender = payload.gender
        member.dob = payload.dob
        member.state = payload.state
        member.district = payload.district
        member.pincode = payload.pincode
        member.mobile = payload.mobile
        member.blood_group = payload.blood_group
        member.whatsapp_notification = payload.whatsapp_notification
        member.candidate_type = payload.candidate_type

        db.commit()
        db.refresh(member)

        return member