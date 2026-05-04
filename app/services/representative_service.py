from fastapi import HTTPException
from app.models.member import Member
from app.repositories.representative_repository import RepresentativeRepository


class RepresentativeService:

    @staticmethod
    def create_university(db, payload):

        member = db.query(Member).filter_by(
            membership_id=payload.membership_id
        ).first()

        if not member:
            raise HTTPException(status_code=404, detail="Member not found")

        data = payload.dict()
        data["member_id"] = member.id
        data.pop("membership_id", None)

        return RepresentativeRepository.create_university(db, data)


    @staticmethod
    def create_autonomous(db, payload):

        member = db.query(Member).filter_by(
            membership_id=payload.membership_id
        ).first()

        if not member:
            raise HTTPException(status_code=404, detail="Member not found")

        data = payload.dict()
        data["member_id"] = member.id
        data.pop("membership_id", None)

        return RepresentativeRepository.create_autonomous(db, data)


    @staticmethod
    def create_both(db, payload):

        member = db.query(Member).filter_by(
            membership_id=payload.membership_id
        ).first()

        if not member:
            raise HTTPException(status_code=404, detail="Member not found")

        data = payload.dict()
        data["member_id"] = member.id
        data.pop("membership_id", None)

        return RepresentativeRepository.create_both(db, data)