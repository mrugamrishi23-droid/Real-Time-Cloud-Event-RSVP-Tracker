import os
os.environ["DATABASE_URL"]="sqlite:///./test_event_tracker.db"
from fastapi.testclient import TestClient
from app.main import app

client=TestClient(app)

def register(email, role="ATTENDEE"):
    r=client.post("/api/register",json={"name":"Test User","email":email,"password":"secret123","role":role})
    assert r.status_code==200
    return r.json()["access_token"]

def test_register_and_login():
    email="user1@example.com"
    token=register(email)
    r=client.post("/api/login",json={"email":email,"password":"secret123"})
    assert r.status_code==200
    assert token

def test_duplicate_registration():
    email="dup@example.com"
    register(email)
    r=client.post("/api/register",json={"name":"Test","email":email,"password":"secret123","role":"ATTENDEE"})
    assert r.status_code==409
