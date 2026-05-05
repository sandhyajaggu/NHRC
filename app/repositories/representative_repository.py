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

        results = db.query(
            Member.membership_id,
            Member.full_name,
            Member.mobile,
            Member.status,

            func.coalesce(
                RepresentativeUniversityDetails.designation,
                RepresentativeAutonomousDetails.designation,
                RepresentativeBothDetails.designation
            ).label("designation")

        ).outerjoin(
            RepresentativeUniversityDetails,
            RepresentativeUniversityDetails.member_id == Member.id
        ).outerjoin(
            RepresentativeAutonomousDetails,
            RepresentativeAutonomousDetails.member_id == Member.id
        ).outerjoin(
            RepresentativeBothDetails,
            RepresentativeBothDetails.member_id == Member.id
        ).filter(
            Member.candidate_type == "representative"
        ).all()

        return [
            {
                "membership_id": row.membership_id,
                "name": row.full_name,
                "phone": row.mobile,
                "status": row.status,
                "designation": row.designation
            }
            for row in results
        ]