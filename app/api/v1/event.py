from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.service_event import ServiceEvent
from app.services.event_service import EventService

router = APIRouter(
    prefix="/events",
    tags=["Events"]
)


@router.get("/service/{service_id}")
def get_events(
    service_id: int,
    db: Session = Depends(get_db)
):

    events = db.query(ServiceEvent).filter(
        ServiceEvent.service_id == service_id
    ).all()

    return events
@router.get("/counts/{event_id}")
def get_counts(
    event_id: int,
    db: Session = Depends(get_db)
):

    return EventService.get_event_counts(
        db,
        event_id
    )
@router.get("/search")
def search_events(
    search: str = None,
    db: Session = Depends(get_db)
):

    return EventService.search_events(
        db,
        search
    )

