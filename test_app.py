import pytest
from app import app, itineraries


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_add_itinerary(client):
    response = client.post(
        "/add",
        data={
            "destination": "Pune",
            "day": "Day 2",
            "activity": "Visit Shaniwar Wada",
            "notes": "Morning visit"
        }
    )

    assert response.status_code == 302
    assert itineraries[-1]["destination"] == "Pune"
    assert itineraries[-1]["activity"] == "Visit Shaniwar Wada"


def test_invalid_itinerary(client):
    response = client.post(
        "/add",
        data={
            "destination": "",
            "day": "Day 2",
            "activity": "",
            "notes": ""
        }
    )

    assert response.status_code == 400
