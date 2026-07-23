import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database import Base, get_db
from backend.main import app
from backend.models.event import Event


TEST_DATABASE_URL = "postgresql+psycopg://ay@localhost/event_scout_test"

test_engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False,
)

Base.metadata.create_all(bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_test_database():
    db = TestingSessionLocal()

    try:
        db.query(Event).delete()
        db.commit()
    finally:
        db.close()


def create_test_event():
    response = client.post(
        "/events",
        json={
            "title": "Original Event",
            "city": "Los Angeles",
            "category": "Basketball",
            "date": "2026-10-01",
            "venue": "Test Arena",
            "description": "Created by pytest",
        },
    )

    assert response.status_code == 201

    return response.json()


def test_create_event():
    response = client.post(
        "/events",
        json={
            "title": "Test Event",
            "city": "Los Angeles",
            "category": "Basketball",
            "date": "2026-10-01",
            "venue": "Test Arena",
            "description": "Created by pytest",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Test Event"
    assert data["city"] == "Los Angeles"
    assert "id" in data


def test_patch_existing_event():
    event = create_test_event()

    response = client.patch(
        f"/events/{event['id']}",
        json={"title": "Updated Event"},
    )

    assert response.status_code == 200
    assert response.json() == {
        **event,
        "title": "Updated Event",
    }


def test_delete_existing_event():
    event = create_test_event()

    delete_response = client.delete(f"/events/{event['id']}")

    assert delete_response.status_code == 204

    get_response = client.get(f"/events/{event['id']}")

    assert get_response.status_code == 404
    assert get_response.json() == {"detail": "Event not found"}


def test_patch_nonexistent_event():
    response = client.patch(
        "/events/999999999",
        json={"title": "Updated Event"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Event not found"}


def test_delete_nonexistent_event():
    response = client.delete("/events/999999999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Event not found"}
