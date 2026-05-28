from fastapi import HTTPException

from app.models.event_registration import EventRegistration
from app.models.service import Service
from app.models.service_event import ServiceEvent


class EventService:

    @staticmethod
    def create_event(db, payload, banner_image=None):

        service = db.query(Service).filter(
            Service.id == payload.service_id
        ).first()

        if not service:
            raise HTTPException(
                status_code=404,
                detail="Service not found"
            )

        event = ServiceEvent(

            service_id=payload.service_id,

            title=payload.title,

            description=payload.description,

            program_category=payload.program_category,

            speaker_name=payload.speaker_name,

            organizer_name=payload.organizer_name,

            event_mode=payload.event_mode,

            start_date=payload.start_date,

            end_date=payload.end_date,

            start_time=payload.start_time,

            end_time=payload.end_time,

            location=payload.location,

            banner_image=banner_image
        )

        db.add(event)

        db.commit()

        db.refresh(event)

        return {
            "message": "Event created successfully",
            "event_id": event.id
        }
    @staticmethod
    def get_event_counts(db, event_id: int):

        student_count = db.query(EventRegistration).filter(
            EventRegistration.event_id == event_id,
            EventRegistration.member_type == "student"
        ).count()

        hr_count = db.query(EventRegistration).filter(
            EventRegistration.event_id == event_id,
            EventRegistration.member_type == "hr"
        ).count()

        return {
            "student_count": student_count,
            "hr_count": hr_count
        }
    @staticmethod
    def search_events(
        db,
        search: str = None
    ):

        query = db.query(ServiceEvent)

        if search:
            query = query.filter(
                ServiceEvent.title.ilike(f"%{search}%")
            )

        return query.all()
    @staticmethod
    def delete_event(db, event_id: int):

        event = db.query(ServiceEvent).filter(
            ServiceEvent.id == event_id
        ).first()

        if not event:
            raise HTTPException(
                status_code=404,
                detail="Event not found"
            )

        db.delete(event)

        db.commit()

        return {
            "message": "Event deleted successfully"
        }
    @staticmethod
    def get_events(db):

        return db.query(ServiceEvent).filter(
            ServiceEvent.event_type == "EVENT"
        ).all()
    @staticmethod
    def get_training_programs(db):

        return db.query(ServiceEvent).filter(
            ServiceEvent.event_type == "TRAINING"
        ).all()
    @staticmethod
    def get_job_fairs(db):

        return db.query(ServiceEvent).filter(
            ServiceEvent.event_type == "JOB_FAIR"
        ).all()