# tests/test_tcapi.py

from fastapi.testclient import TestClient
from TCApi import app  # Make sure this matches your filename exactly

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from Dockerized FastAPI!"}