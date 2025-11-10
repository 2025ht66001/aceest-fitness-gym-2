import json
from app import create_app

def test_health():
    app = create_app()
    client = app.test_client()
    r = client.get("/healthz")
    assert r.status_code == 200
    assert b"ok" in r.data

def test_crud_workout():
    app = create_app()
    client = app.test_client()

    # create
    r = client.post("/api/workouts", json={"name": "Run", "duration": 30, "calories": 250})
    assert r.status_code == 201
    item = r.get_json()
    assert item["id"] == 1

    # list
    r = client.get("/api/workouts")
    assert r.status_code == 200
    items = r.get_json()
    assert len(items) == 1

    # get
    r = client.get("/api/workouts/1")
    assert r.status_code == 200
    assert r.get_json()["name"] == "Run"

    # delete
    r = client.delete("/api/workouts/1")
    assert r.status_code == 204

    # get 404
    r = client.get("/api/workouts/1")
    assert r.status_code == 404
