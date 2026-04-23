from sqlalchemy.orm import Session
from app.models.contact import ContactMessage


class ContactRepository:

    @staticmethod
    def create(db: Session, payload: dict):
        contact = ContactMessage(**payload)

        db.add(contact)
        db.commit()
        db.refresh(contact)

        return contact