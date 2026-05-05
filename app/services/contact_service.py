from sqlalchemy.orm import Session
from app.repositories.contact_repository import ContactRepository
from fastapi import HTTPException


class ContactService:

    @staticmethod
    def create_contact(db: Session, payload):
        return ContactRepository.create(db, payload)

    @staticmethod
    def get_all_contacts(db: Session):
        return ContactRepository.get_all(db)

    #  FIXED: use ID
    @staticmethod
    def get_contact_by_id(db: Session, contact_id: int):
        contact = ContactRepository.get_by_id(db, contact_id)

        if not contact:
            raise HTTPException(status_code=404, detail="Contact not found")

        return contact

    #  FIXED: use ID
    from fastapi import HTTPException



    @staticmethod
    def delete_contact(db, contact_id: int):
        print("Deleting contact_id:", contact_id)

        contact = ContactRepository.delete_by_id(db, contact_id)

        print("Contact found:", contact)

        if not contact:
            raise HTTPException(status_code=404, detail="Contact not found")

        return {"message": "Contact deleted successfully"}