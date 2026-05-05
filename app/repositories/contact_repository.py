# app/repositories/contact_repository.py

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

    @staticmethod
    def get_all(db: Session):
        return db.query(ContactMessage).all()

    @staticmethod
    def get_by_membership_id(db: Session, membership_id: str):
        return db.query(ContactMessage).filter(
            ContactMessage.membership_id == membership_id
        ).first()

    @staticmethod
    def delete_by_membership_id(db: Session, membership_id: str):
        contact = db.query(ContactMessage).filter(
            ContactMessage.membership_id == membership_id
        ).first()

        if contact:
            db.delete(contact)
            db.commit()

        return contact