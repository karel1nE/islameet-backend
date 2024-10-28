import pytest
from fastapi.testclient import TestClient
from app.models.user import User
from sqlalchemy.orm import Session


@pytest.mark.usefixtures("client")
def test_create_user(client):
    response = client.post(
        "/api/users/",
        json={"username": "testuser", "email": "test@example.com", "full_name": "Test User"},
    )
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

@pytest.mark.usefixtures("client")
def test_read_user(client):    
    response = client.get("/api/users/1")  
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_update_user(client):
    response = client.put(
        "/api/users/1",
        json={"username": "updateduser", "email": "updated@example.com", "full_name": "Updated User"},
    )
    assert response.status_code == 200
    assert response.json()["username"] == "updateduser"

def test_delete_user(client):
    response = client.delete("/api/users/1")
    assert response.status_code == 200
    assert response.json() == {"message": "User deleted"}

    response = client.get("/api/users/1")
    assert response.status_code == 400