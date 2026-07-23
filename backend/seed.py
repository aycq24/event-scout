from sqlalchemy import select

from backend.database import Base, SessionLocal, engine
from backend.models.event import Event


initial_events = [
    {
        "title": "FIFA World Cup Final",
        "city": "New York",
        "category": "Sports",
        "date": "July 19, 2026",
        "venue": "MetLife Stadium",
        "description": "Watch the biggest international football match of the year.",
    },
    {
        "title": "Taylor Swift Concert",
        "city": "Los Angeles",
        "category": "Concerts",
        "date": "August 8, 2026",
        "venue": "SoFi Stadium",
        "description": "A major live concert experience.",
    },
    {
        "title": "NBA Finals",
        "city": "San Francisco",
        "category": "Sports",
        "date": "June 16, 2026",
        "venue": "Chase Center",
        "description": "Experience the intensity of the NBA Finals live.",
    },
    {
        "title": "Anime Expo",
        "city": "Los Angeles",
        "category": "Entertainment",
        "date": "July 2, 2026",
        "venue": "Los Angeles Convention Center",
        "description": "Explore anime, manga, gaming, cosplay, and pop culture.",
    },
]


def seed_database():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        existing_event = db.scalar(
            select(Event).limit(1)
        )

        if existing_event:
            print("Events already exist. Seed skipped.")
            return

        event_objects = [
            Event(**event_data)
            for event_data in initial_events
        ]

        db.add_all(event_objects)
        db.commit()

        print(f"Successfully inserted {len(event_objects)} events.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()