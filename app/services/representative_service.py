from fastapi import HTTPException
from app.repositories.representative_repository import RepresentativeRepository
from app.models.member import Member


class RepresentativeService:

    @staticmethod
    def create_university(db, payload, member_id):
        data = payload.dict()
        data.pop("membership_id", None)
        data["member_id"] = member_id

        return RepresentativeRepository.create_university(db, data)

    @staticmethod
    def create_autonomous(db, payload, member_id):
        data = payload.dict()
        data.pop("membership_id", None)
        data["member_id"] = member_id

        return RepresentativeRepository.create_autonomous(db, data)

    @staticmethod
    def create_both(db, payload, member_id):
        data = payload.dict()
        data.pop("membership_id", None)
        data["member_id"] = member_id

        return RepresentativeRepository.create_both(db, data)