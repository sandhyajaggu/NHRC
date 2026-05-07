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
        obj = RepresentativeUniversityDetails(**data)
        db.add(obj)
        db.commit()
        db.refresh(obj)
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

        results = []

        university = db.query(
            Member,
            RepresentativeUniversityDetails
        ).join(
            RepresentativeUniversityDetails,
            RepresentativeUniversityDetails.member_id == Member.id
        ).filter(
            Member.candidate_type == "representative"
        ).all()

        autonomous = db.query(
            Member,
            RepresentativeAutonomousDetails
        ).join(
            RepresentativeAutonomousDetails,
            RepresentativeAutonomousDetails.member_id == Member.id
        ).filter(
            Member.candidate_type == "representative"
        ).all()

        both = db.query(
            Member,
            RepresentativeBothDetails
        ).join(
            RepresentativeBothDetails,
            RepresentativeBothDetails.member_id == Member.id
        ).filter(
            Member.candidate_type == "representative"
        ).all()

        for member, details in university:
            results.append({
                "member": member,
                "details": details
            })

        for member, details in autonomous:
            results.append({
                "member": member,
                "details": details
            })

        for member, details in both:
            results.append({
                "member": member,
                "details": details
            })

        return jsonable_encoder(results)