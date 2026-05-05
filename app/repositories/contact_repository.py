# app/repositories/contact_repository.py

from sqlalchemy.orm import Session
from app.models.contact import Contact


class ContactRepository:

    @staticmethod
    def create(db: Session, payload: dict):
        contact = Contact(**payload)
        db.add(contact)
        db.commit()
        db.refresh(contact)
        return contact

    @staticmethod
    def get_all(db: Session):
        return db.query(Contact).all()

    @staticmethod
    def get_by_membership_id(db: Session, membership_id: str):
        return db.query(Contact).filter(
            Contact.membership_id == membership_id
        ).first()

    @staticmethod
    def delete_by_membership_id(db: Session, membership_id: str):
        contact = db.query(Contact).filter(
            Contact.membership_id == membership_id
        ).first()

        if contact:
            db.delete(contact)
            db.commit()

        return contact