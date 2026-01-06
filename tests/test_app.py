import uuid
from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # known activity from seed data
    assert "Chess Club" in data


def test_signup_and_unregister():
    activity = "Chess Club"
    email = f"test-{uuid.uuid4().hex[:8]}@example.com"

    # signup
    r = client.post(f"/activities/{activity}/signup?email={email}")
    assert r.status_code == 200
    assert "Signed up" in r.json().get("message", "")

    # verify present
    r2 = client.get("/activities")
    assert email in r2.json()[activity]["participants"]

    # unregister
    r3 = client.post(f"/activities/{activity}/unregister?email={email}")
    assert r3.status_code == 200
    assert "Unregistered" in r3.json().get("message", "")

    # verify removed
    r4 = client.get("/activities")
    assert email not in r4.json()[activity]["participants"]
