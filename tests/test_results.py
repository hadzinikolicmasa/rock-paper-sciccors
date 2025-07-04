import pytest
from app.database import SessionLocal
from app.database.models.match import Match
from app.database.models.player import Player

@pytest.fixture
def test_player():
    db = SessionLocal()
    player = Player(username="test_results_user")
    db.add(player)
    db.commit()
    db.refresh(player)
    yield player
    db.query(Match).delete()
    db.query(Player).filter_by(id=player.id).delete()
    db.commit()
    db.close()

@pytest.fixture
def test_match(test_player):
    db = SessionLocal()
    match = Match(
        player1_id=test_player.id,
        player1_choice="rock",
        player2_choice="scissors",
        winner_id=test_player.id,
        completed=True
    )
    db.add(match)
    db.commit()
    db.refresh(match)
    yield match
    db.query(Match).filter_by(id=match.id).delete()
    db.commit()
    db.close()

def test_results_empty(client, test_player):
    res = client.post("/results", json={"username": test_player.username})
    assert res.status_code == 200
    data = res.get_json()
    assert isinstance(data, list)
    assert len(data) == 0

def test_results_missing_data(client):
    res = client.post("/results", json={})
    data = res.get_json()

    assert res.status_code == 400
    assert data["error"] == "Username is required"


def test_results_user_not_found(client):
    res = client.post("/results", json={"username": "user_not_found"})
    data = res.get_json()

    assert res.status_code == 404
    assert data["error"] == "Player not found"


def test_results_with_matches(client, test_player, test_match):
    res = client.post("/results", json={"username": test_player.username})
    assert res.status_code == 200
    data = res.get_json()
    assert len(data) == 1
    assert data[0]["your_choice"] == "rock"
    assert data[0]["result"] == "win"

def test_reset_results_user_not_found(client):
    res = client.delete("/results/reset", json={"username": "user_not_found"})
    data = res.get_json()

    assert res.status_code == 404
    assert data["error"] == "User not found"


def test_reset_results_missing_data(client):
    res = client.delete("/results/reset", json={})
    data = res.get_json()

    assert res.status_code == 400
    assert data["error"] == "Username is required"


def test_reset_results(client, test_player, test_match):
    res = client.delete("/results/reset", json={"username": test_player.username})
    assert res.status_code == 200
    msg = res.get_json()
    assert msg["message"] == "Results cleared!"

    res2 = client.post("/results", json={"username": test_player.username})
    assert res2.status_code == 200
    assert res2.get_json() == []