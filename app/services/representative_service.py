from fastapi import HTTPException
from app.models.member import Member
from app.repositories.representative_repository import RepresentativeRepository


class RepresentativeService:

    @staticmethod
    def _get_member_id(db, membership_id: str):
        member = db.query(Member).filter_by(
            membership_id=membership_id
        ).first()

        if not member:
            print(" MEMBER NOT FOUND:", membership_id)
            raise HTTPException(status_code=404, detail="Member not found")

        return member.id


    @staticmethod
    def _prepare_data(payload, member_id):
        data = payload.dict()
        data["member_id"] = member_id
        data.pop("membership_id", None)
        return data


    @staticmethod
    def _build_response(message, obj):
        return {
            "message": message,
            "id": obj.id,
            "member_id": obj.member_id,
            "college_name": obj.college_name,
            "university_name": getattr(obj, "university_name", None),
            "college_code": obj.college_code,
            "designation": obj.designation,
            "department": obj.department,
            "state": obj.state,
            "district": obj.district,
            "pincode": obj.pincode,
            "experience": obj.experience,
            "official_mail_id": obj.official_mail_id,
            "mobile_number": obj.mobile_number
        }


    # 🔹 UNIVERSITY
    @staticmethod
    def create_university(db, payload):
        member_id = RepresentativeService._get_member_id(db, payload.membership_id)
        data = RepresentativeService._prepare_data(payload, member_id)

        obj = RepresentativeRepository.create_university(db, data)

        return RepresentativeService._build_response(
            "Representative (University) created successfully",
            obj
        )


    # 🔹 AUTONOMOUS
    @staticmethod
    def create_autonomous(db, payload):
        member_id = RepresentativeService._get_member_id(db, payload.membership_id)
        data = RepresentativeService._prepare_data(payload, member_id)

        obj = RepresentativeRepository.create_autonomous(db, data)

        return RepresentativeService._build_response(
            "Representative (Autonomous) created successfully",
            obj
        )


    # 🔹 BOTH
    @staticmethod
    def create_both(db, payload):
        member_id = RepresentativeService._get_member_id(db, payload.membership_id)
        data = RepresentativeService._prepare_data(payload, member_id)

        obj = RepresentativeRepository.create_both(db, data)

        return RepresentativeService._build_response(
            "Representative (Both) created successfully",
            obj
        )
    