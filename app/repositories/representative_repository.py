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