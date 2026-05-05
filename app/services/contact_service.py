# app/services/contact_service.py

from sqlalchemy.orm import Session
from app.repositories.contact_repository import ContactRepository


class ContactService:

    @staticmethod
    def create_contact(db: Session, payload):
        return ContactRepository.create(db, payload.dict())

    @staticmethod
    def get_all_contacts(db: Session):
        return ContactRepository.get_all(db)

    @staticmethod
    def get_contact_by_membership_id(db: Session, membership_id: str):
        contact = ContactRepository.get_by_membership_id(db, membership_id)

        if not contact:
            raise Exception("Contact not found")

        return contact

    @staticmethod
    def delete_contact(db: Session, membership_id: str):
        contact = ContactRepository.delete_by_membership_id(db, membership_id)

        if not contact:
            raise Exception("Contact not found")

        return {"message": "Contact deleted successfully"}