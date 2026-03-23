import os
from pathlib import Path

from fastapi.testclient import TestClient

TEST_DB_PATH = Path(__file__).resolve().parent / "test_auth.db"

if TEST_DB_PATH.exists():
    TEST_DB_PATH.unlink()

os.environ["APP_NAME"] = "Mastermind API Test"
os.environ["APP_ENV"] = "test"
os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB_PATH.as_posix()}"
os.environ["JWT_SECRET"] = "test-secret"
os.environ["JWT_ALGORITHM"] = "HS256"
os.environ["JWT_EXPIRE_MINUTES"] = "1440"
os.environ["CORS_ALLOWED_ORIGINS"] = "http://localhost:4200"

from main import app

client = TestClient(app)


def test_register_and_login_flow():
    register_response = client.post(
        "/api/auth/register",
        json={
            "email": "player@example.com",
            "full_name": "Player One",
            "password": "secret123",
        },
    )

    assert register_response.status_code == 201
    register_body = register_response.json()
    assert register_body["email"] == "player@example.com"
    assert register_body["full_name"] == "Player One"
    assert register_body["is_active"] is True
    assert "hashed_password" not in register_body

    login_response = client.post(
        "/api/auth/login",
        json={
            "email": "player@example.com",
            "password": "secret123",
        },
    )

    assert login_response.status_code == 200
    login_body = login_response.json()
    assert login_body["token_type"] == "bearer"
    assert login_body["access_token"]
    assert login_body["user"]["email"] == "player@example.com"
