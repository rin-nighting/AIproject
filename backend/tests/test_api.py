import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_poll():
    response = client.get("/api/poll")
    assert response.status_code == 200
    data = response.json()
    assert "question" in data
    assert "options" in data
    assert isinstance(data["options"], list)

def test_vote():
    poll = client.get("/api/poll").json()
    option_id = poll["options"][0]["id"]
    response = client.post("/api/poll/vote", json={
        "poll_id": poll["id"],
        "option_id": option_id
    })
    assert response.status_code == 200
    assert response.json()["success"] is True 