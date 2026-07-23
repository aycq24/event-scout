from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.services import events_service
from backend.schemas.event import EventCreate, EventResponse

router = APIRouter()


@router.get("/events")
def get_events(
    search: str = "",
    category: str = "All",
    db: Session = Depends(get_db),
):
    return events_service.get_events(
        db=db,
        search=search,
        category=category,
    )


@router.get("/events/{event_id}")
def get_event(
    event_id: int,
    db: Session = Depends(get_db),
):
    event = events_service.get_event_by_id(
        db=db,
        event_id=event_id,
    )

    if event is None:
        raise HTTPException(
            status_code=404,
            detail="Event not found",
        )

    return event



@router.post(
    "/events",
    response_model=EventResponse,
    status_code=201,
)
def create_event(
    event_data: EventCreate,
    db: Session = Depends(get_db),
):
    return events_service.create_event(db, event_data)