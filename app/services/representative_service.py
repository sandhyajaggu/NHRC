from app.repositories.representative_repository import RepresentativeRepository


class RepresentativeService:

    @staticmethod
    def create_university(db, payload):
        data = payload.dict(exclude={
            "university_address"  # not in DB
        })
        return RepresentativeRepository.create_university(db, payload)

    @staticmethod
    def create_autonomous(db, payload):
        data = payload.dict(exclude={
            "college_address"
        })
        return RepresentativeRepository.create_autonomous(db, payload)

    @staticmethod
    def create_both(db, payload):
        data = payload.dict(exclude={
            "confirm_password"
        })
        return RepresentativeRepository.create_both(db, payload)