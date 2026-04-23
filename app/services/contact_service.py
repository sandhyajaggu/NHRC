from app.repositories.contact_repository import ContactRepository


class ContactService:

    @staticmethod
    def create_message(db, payload):
        return ContactRepository.create(
            db,
            payload.dict()
        )