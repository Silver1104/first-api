import stat
from venv import create
from app import schemas
import pytest
from jose import jwt
from app.config import settings

def test_create_user(client):
    res = client.post(
        "/users/", json={"name": "hello123", "email": "hello123@gmail.com", "password": "password123"})

    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201

def test_login_user(client, test_user):
    res = client.post("/login", data = {"username": test_user["email"], "password": test_user["password"]})   
    assert res.status_code == 200
    token_data = res.json()
    assert "access_token" in token_data
    assert "token_type" in token_data
    assert token_data["token_type"] == "bearer"
    decoded_jwt = jwt.decode(token_data["access_token"], settings.secret_key, algorithms=[settings.algorithm])
    id: str = decoded_jwt.get("user_id")
    assert id == test_user['id']

@pytest.mark.parametrize("email, password, status_code", [
    ("invalidemail", "password123", 403),
    ("hello123@gmail.com", "wrongpassword", 403),
    (None, "password123", 403),
    ("hello123@gmail.com", "", 403),
    ("", "", 403),
    ("invalidemail", "wrongpassword", 403),
])
def test_failed_login(client, email, password, status_code):
    res = client.post("/login", data = {"username": email, "password": password})
    assert res.status_code == status_code
    assert res.json().get("detail") == "Invalid credentials"

def test_successful_login(client, test_user):
    """Test successful login with valid credentials"""
    res = client.post("/login", data = {"username": test_user["email"], "password": test_user["password"]})
    assert res.status_code == 200
    token_data = res.json()
    assert "access_token" in token_data
    assert "token_type" in token_data
    assert token_data["token_type"] == "bearer"