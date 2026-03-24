import os
from pathlib import Path

from fastapi.testclient import TestClient

TEST_DB_PATH = Path(__file__).resolve().parent / "test_games.db"

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
from app.db.session import SessionLocal
from app.models.game import Game

client = TestClient(app)


def test_create_game_requires_auth_and_returns_public_fields_only():
    register_response = client.post(
        "/api/auth/register",
        json={
            "email": "gamer@example.com",
            "full_name": "Gamer One",
            "password": "secret123",
        },
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/api/auth/login",
        json={
            "email": "gamer@example.com",
            "password": "secret123",
        },
    )

    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    create_response = client.post(
        "/api/games",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert create_response.status_code == 201
    body = create_response.json()
    assert len(body["code"]) == 8
    assert body["remaining_attempts"] == 10
    assert body["is_finished"] is False
    assert body["is_won"] is False
    assert body["final_score"] == 0
    assert body["duration_seconds"] == 0
    assert "secret_code" not in body


def test_make_guess_returns_progress_and_can_win_game():
    register_response = client.post(
        "/api/auth/register",
        json={
            "email": "player2@example.com",
            "full_name": "Player Two",
            "password": "secret123",
        },
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/api/auth/login",
        json={
            "email": "player2@example.com",
            "password": "secret123",
        },
    )

    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    create_response = client.post(
        "/api/games",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert create_response.status_code == 201
    game_code = create_response.json()["code"]

    db = SessionLocal()
    try:
        game = db.query(Game).filter(Game.code == game_code).first()
        assert game is not None
        game.secret_code = "RGBY"
        db.commit()
    finally:
        db.close()

    guess_response = client.post(
        f"/api/games/{game_code}/guess",
        headers={"Authorization": f"Bearer {token}"},
        json={"guess": "RGBY"},
    )

    assert guess_response.status_code == 200
    body = guess_response.json()
    assert body["correct_count"] == 4
    assert body["remaining_attempts"] == 9
    assert body["is_finished"] is True
    assert body["is_won"] is True


def test_get_game_and_list_attempts_returns_history_for_owner():
    register_response = client.post(
        "/api/auth/register",
        json={
            "email": "history@example.com",
            "full_name": "History Player",
            "password": "secret123",
        },
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/api/auth/login",
        json={
            "email": "history@example.com",
            "password": "secret123",
        },
    )

    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    create_response = client.post(
        "/api/games",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert create_response.status_code == 201
    game_code = create_response.json()["code"]

    db = SessionLocal()
    try:
        game = db.query(Game).filter(Game.code == game_code).first()
        assert game is not None
        game.secret_code = "RGBY"
        db.commit()
    finally:
        db.close()

    first_guess_response = client.post(
        f"/api/games/{game_code}/guess",
        headers={"Authorization": f"Bearer {token}"},
        json={"guess": "RRRR"},
    )

    assert first_guess_response.status_code == 200

    game_response = client.get(
        f"/api/games/{game_code}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert game_response.status_code == 200
    game_body = game_response.json()
    assert game_body["code"] == game_code
    assert game_body["remaining_attempts"] == 9
    assert game_body["is_finished"] is False
    assert game_body["is_won"] is False
    assert game_body["final_score"] == 0

    attempts_response = client.get(
        f"/api/games/{game_code}/attempts",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert attempts_response.status_code == 200
    attempts_body = attempts_response.json()
    assert len(attempts_body) == 1
    assert attempts_body[0]["guess"] == "RRRR"
    assert attempts_body[0]["correct_count"] == 1


def test_ranking_returns_players_ordered_by_best_score():
    register_response = client.post(
        "/api/auth/register",
        json={
            "email": "ranker@example.com",
            "full_name": "Ranker Player",
            "password": "secret123",
        },
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/api/auth/login",
        json={
            "email": "ranker@example.com",
            "password": "secret123",
        },
    )

    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    create_response = client.post(
        "/api/games",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert create_response.status_code == 201
    game_code = create_response.json()["code"]

    db = SessionLocal()
    try:
        game = db.query(Game).filter(Game.code == game_code).first()
        assert game is not None
        game.secret_code = "RGBY"
        db.commit()
    finally:
        db.close()

    guess_response = client.post(
        f"/api/games/{game_code}/guess",
        headers={"Authorization": f"Bearer {token}"},
        json={"guess": "RGBY"},
    )

    assert guess_response.status_code == 200

    game_response = client.get(
        f"/api/games/{game_code}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert game_response.status_code == 200
    assert game_response.json()["final_score"] > 0
    assert game_response.json()["duration_seconds"] >= 0

    ranking_response = client.get(
        "/api/games/ranking/list",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert ranking_response.status_code == 200
    ranking_body = ranking_response.json()
    assert len(ranking_body) >= 1
    ranker_entry = next((entry for entry in ranking_body if entry["email"] == "ranker@example.com"), None)
    assert ranker_entry is not None
    assert ranker_entry["best_score"] > 0
    assert ranker_entry["wins"] >= 1
