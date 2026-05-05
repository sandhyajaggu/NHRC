# app/repositories/contact_repository.py

from sqlalchemy.orm import Session
from app.models.contact import ContactMessage


class ContactRepository:

    @staticmethod
    def create(db: Session, data: dict):
        contact = ContactMessage(**data)
        db.add(contact)
        db.commit()
        db.refresh(contact)
        return contact

    @staticmethod
    def get_all(db: Session):
        return db.query(ContactMessage).all()

    @staticmethod
    def get_by_id(db: Session, contact_id: int):
        return db.query(ContactMessage).filter(ContactMessage.id == contact_id).first()


@staticmethod
def delete_by_id(db: Session, contact_id: int):
    contact = db.query(ContactMessage).filter(ContactMessage.id == contact_id).first()

    if not contact:
        return False

    db.delete(contact)
    db.commit()
    return True