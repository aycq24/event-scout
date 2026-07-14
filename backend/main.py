from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Hello Event Scout!"}


events = [
    {
        "id": 1,
        "title": "FIFA World Cup Final",
        "city": "New York",
        "category": "Sports",
        "date": "July 19, 2026",
        "venue": "MetLife Stadium",
        "description": "Watch the biggest international football match of the year.",
    },
    {
        "id": 2,
        "title": "Taylor Swift Concert",
        "city": "Los Angeles",
        "category": "Concerts",
        "date": "August 8, 2026",
        "venue": "SoFi Stadium",
        "description": "A major live concert experience.",
    },
    {
        "id": 3,
        "title": "NBA Finals",
        "city": "San Francisco",
        "category": "Sports",
        "date": "June 16, 2026",
        "venue": "Chase Center",
        "description": "Experience the intensity of the NBA Finals live.",
    },
    {
        "id": 4,
        "title": "Anime Expo",
        "city": "Los Angeles",
        "category": "Entertainment",
        "date": "July 2, 2026",
        "venue": "Los Angeles Convention Center",
        "description": "Explore anime, manga, gaming, cosplay, and pop culture.",
    },
]


@app.get("/events")
def get_events(search: str = "", category: str = "All"):
    filtered = []

    for event in events:
        matches_search = search.lower() in event["title"].lower()

        matches_category = (
            category == "All"
            or event["category"] == category
        )

        if matches_search and matches_category:
            filtered.append(event)

    return filtered


@app.get("/events/{event_id}")
def get_event(event_id: int):
    for event in events:
        if event["id"] == event_id:
            return event

    raise HTTPException(
        status_code=404,
        detail="Event not found",
    )
