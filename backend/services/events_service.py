from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.event import Event
from backend.schemas.event import EventCreate

def get_events(
    db: Session,
    search: str = "",
    category: str = "All",
):
    statement = select(Event)

    if search:
        statement = statement.where(
            Event.title.ilike(f"%{search}%")
        )

    if category != "All":
        statement = statement.where(
            Event.category == category
        )

    statement = statement.order_by(Event.id)

    return db.scalars(statement).all()


def get_event_by_id(
    db: Session,
    event_id: int,
):
    return db.get(Event, event_id)




def create_event(db: Session, event_data: EventCreate) -> Event:
    event = Event(**event_data.model_dump())

    db.add(event)
    db.commit()
    db.refresh(event)

    return event