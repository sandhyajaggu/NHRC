from datetime import datetime

from fastapi import HTTPException

from app.models.service_event import ServiceEvent
from app.models.event_registration import EventRegistration


class RegistrationService:

    @staticmethod
    def register_event(db, payload):

        event = db.query(ServiceEvent).filter(
            ServiceEvent.id == payload.event_id
        ).first()

        if not event:
            raise HTTPException(
                status_code=404,
                detail="Event not found"
            )

        registration = EventRegistration(

            event_id=payload.event_id,

            member_id=payload.member_id,

            member_type=payload.member_type,

            full_name=payload.full_name,

            email=payload.email,

            phone=payload.phone,

            location=payload.location,

            nhrc_id=payload.nhrc_id,

            college_name=payload.college_name,

            year_of_passout=payload.year_of_passout,

            company_name=payload.company_name,

            company_location=payload.company_location,

            company_url=payload.company_url
        )

        db.add(registration)

        db.commit()

        db.refresh(registration)

        return {
            "message": "Registered successfully",
            "registration_id": registration.id
        }

class RegistrationManagementService:

    @staticmethod
    def approve_registration(db, registration_id: int):

        registration = db.query(EventRegistration).filter(
            EventRegistration.id == registration_id
        ).first()

        if not registration:
            raise HTTPException(
                status_code=404,
                detail="Registration not found"
            )

        registration.status = "Approved"

        registration.approved_at = datetime.utcnow()

        db.commit()

        return {
            "message": "Registration approved successfully"
        }

    @staticmethod
    def reject_registration(db, registration_id: int):

        registration = db.query(EventRegistration).filter(
            EventRegistration.id == registration_id
        ).first()

        if not registration:
            raise HTTPException(
                status_code=404,
                detail="Registration not found"
            )

        registration.status = "Rejected"

        db.commit()

        return {
            "message": "Registration rejected successfully"
        }

    @staticmethod
    def forward_registration(
        db,
        registration_id: int,
        forwarded_to: str
    ):

        registration = db.query(EventRegistration).filter(
            EventRegistration.id == registration_id
        ).first()

        if not registration:
            raise HTTPException(
                status_code=404,
                detail="Registration not found"
            )

        registration.status = "Forwarded"

        registration.forwarded_to = forwarded_to

        db.commit()

        return {
            "message": "Registration forwarded successfully"
        }