from fastapi.encoders import jsonable_encoder
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.member import Member
from app.models.representative import (
    RepresentativeUniversityDetails,
    RepresentativeAutonomousDetails,
    RepresentativeBothDetails
)


class RepresentativeRepository:

    @staticmethod
    def create_university(db, data):
        print("SAVING DATA:", data)
        obj = RepresentativeUniversityDetails(**data)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        print("SAVED MEMBER ID:", obj.member_id)
        return obj

    @staticmethod
    def create_autonomous(db, data):
        obj = RepresentativeAutonomousDetails(**data)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    @staticmethod
    def create_both(db, data):
        obj = RepresentativeBothDetails(**data)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    #  NEW METHOD

    @staticmethod
    def get_representatives_with_details(db: Session):

        members = db.query(Member).filter(
            Member.candidate_type == "representative"
        ).all()

        final_data = []

        for member in members:
            print("MEMBER ID:", member.id)

            details = (
                db.query(RepresentativeUniversityDetails)
                .filter(RepresentativeUniversityDetails.member_id == member.id)
                .first()
            )
            print("UNIVERSITY DETAILS:", details)

            if not details:
                details = (
                    db.query(RepresentativeAutonomousDetails)
                    .filter(RepresentativeAutonomousDetails.member_id == member.id)
                    .first()
                )
                print("AUTONOMOUS DETAILS:", details)

            if not details:
                details = (
                    db.query(RepresentativeBothDetails)
                    .filter(RepresentativeBothDetails.member_id == member.id)
                    .first()
                )
                print("BOTH DETAILS:", details)

            final_data.append({
                "member": member,
                "details": details
            })

        return jsonable_encoder(final_data)