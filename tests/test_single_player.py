import pytest
from app.database import SessionLocal
from app.database.models.player import Player

@pytest.fixture
def test_player():
    db = SessionLocal()
    player = Player(username="player1")
    db.add(player)
    db.commit()
    db.refresh(player)
    yield player
    db.query(Player).filter_by(username="player1").delete()
    db.commit()
    db.close()

def test_single_play_missing_data(client):
    res = client.post("/play", json={})
    data = res.get_json()

    assert data["error"] == "You need to select a choice."
    assert res.status_code == 400


def test_single_play_invalid_user(client):
    res = client.post("/play", json={
        "username": "player4",
        "choice_id": 1
    })
    data = res.get_json()
    assert res.status_code == 404
    assert data["error"] == "User not found."


def test_invalid_choice(client, test_player):
    res = client.post("/play", json={"username": "player1", "choice_id": 66})
    data = res.get_json()

    assert res.status_code == 400
    assert data["error"] == "Invalid choice."


def test_single_play_success(client, test_player):
    choices_res = client.get("/choices")
    choice_id = choices_res.get_json()[0]["id"]

    res = client.post("/play", json={
        "username": "player1",
        "choice_id": choice_id
    })
    data = res.get_json()

    assert res.status_code == 200
    assert data["result"] in ["win", "lose", "tie"]
    assert data["computer_choice"]["id"] in [1, 2, 3, 4, 5]
