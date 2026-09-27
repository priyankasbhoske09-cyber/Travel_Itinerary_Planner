import pytest
from app import app, itineraries


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        # Reset memory state before running each test
        itineraries.clear()
        itineraries.append({
            "id": 1,
            "destination": "Goa",
            "day": "Day 1",
            "activity": "Visit Baga Beach",
            "notes": "Evening visit"
        })
        yield client


def test_home_page(client):
    """Test loading the home page."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Travel Itinerary Planner" in response.data


def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_api_itineraries(client):
    """Test getting itineraries as JSON."""
    response = client.get("/api/itineraries")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["destination"] == "Goa"


def test_add_itinerary(client):
    """Test creating a new itinerary item."""
    payload = {
        "destination": "Delhi",
        "day": "Day 2",
        "activity": "Visit Red Fort",
        "notes": "Morning tour"
    }
    response = client.post("/add", data=payload, follow_redirects=True)
    assert response.status_code == 200
    assert b"Delhi" in response.data
    assert b"Visit Red Fort" in response.data


def test_update_itinerary(client):
    """Test updating an itinerary item."""
    payload = {
        "destination": "Goa Updated",
        "day": "Day 1",
        "activity": "Scuba Diving",
        "notes": "Morning slot"
    }
    response = client.post("/update/1", data=payload, follow_redirects=True)
    assert response.status_code == 200
    assert b"Goa Updated" in response.data
    assert b"Scuba Diving" in response.data


def test_delete_itinerary(client):
    """Test removing an itinerary item."""
    response = client.post("/delete/1", follow_redirects=True)
    assert response.status_code == 200
    assert b"Goa" not in response.data
