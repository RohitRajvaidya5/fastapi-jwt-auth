
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_posts(override_database):
    response = client.get("/posts/")

    assert response.status_code == 200
    assert response.json() == []

def test_sample(sample_number):
    assert sample_number == 10

