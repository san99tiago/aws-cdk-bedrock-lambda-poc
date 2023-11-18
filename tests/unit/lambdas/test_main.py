from fastapi.testclient import TestClient
from src.lambdas.main import app

client = TestClient(app)


def test_get_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello by Santi"}


def test_get_status():
    response = client.get("/status")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}


def test_execute_model():
    response = client.post("/model")
    assert response.status_code == 200
    assert response.json() == {"message": "dummy response"}
